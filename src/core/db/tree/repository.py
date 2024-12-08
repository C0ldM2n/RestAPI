import uuid
from typing import TypeVar, Generic, Union

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

# Table model
Model = TypeVar("Model")
# Flexible ID type (int and uuid)
ID = TypeVar("ID", bound=Union[uuid.UUID, int])


class TreeRepository(Generic[Model, ID]):
    """Repository for managing hierarchical tree-like structure"""

    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        """Initialize with model and session"""
        self.model = model
        self.session = session

    async def create_node(self, data) -> Model:
        """Create a new node and adjust tree if necessary."""
        parent_id = data.parent_id

        if parent_id is None:
            # Handle root node creation
            max_rgt = await self.session.execute(
                select(func.max(self.model.rgt))
            )
            max_rgt = max_rgt.scalar() or 0  # Default to 0 if no nodes exist

            # Create the root node
            new_node = self.model(**data)
            new_node.lft = max_rgt + 1
            new_node.rgt = max_rgt + 2
            new_node.level = 0

            self.session.add(new_node)
            await self.session.commit()
            return new_node

        # Handle child node creation
        parent = await self.session.get(self.model, parent_id)
        if not parent:
            raise ValueError(f"Parent node with id {parent_id} not found")

        # Move all nodes after parent's rgt
        await self._shift_nodes(parent.rgt, 2)  # Make space for the new node

        # Create the child node
        new_node = self.model(**data)
        new_node.lft = parent.rgt
        new_node.rgt = parent.rgt + 1
        new_node.level = parent.level + 1

        self.session.add(new_node)
        await self.session.commit()

        # Update parent's rgt
        parent.rgt += 2
        await self.session.commit()

        return new_node

    async def get_by_id(self, node_id: ID) -> Model:
        """Get a node by its ID, including parent and level information"""
        node = await self.session.get(self.model, node_id)
        if not node:
            raise ValueError(f"Node with id {node_id} not found")

        # Optionally, return the node along with parent and level info
        return node

    async def update_node(self, node_id: ID, data) -> None:
        """Update a node, adjust tree if parent_id has changed"""
        # Fetch current node to check if parent_id has changed
        current_node = await self.session.get(self.model, node_id)
        if not current_node:
            raise ValueError(f"Node with id {node_id} not found")

        # Check if parent_id has changed
        parent_id_changed = data.parent_id != current_node.parent_id

        # Check for cyclic reference before updating the node
        if parent_id_changed:
            new_parent_id = data.parent_id
            if new_parent_id:
                await self.validate_no_cycles(node_id, new_parent_id)

        # Update node fields
        for key, value in data.items():
            if key not in ["lft", "rgt", "level"]:  # Prevent overwriting tree-related values
                setattr(current_node, key, value)

        if parent_id_changed:
            new_parent = await self.session.get(self.model, data["parent_id"])
            if not new_parent:
                raise ValueError(f"Parent node with id {data['parent_id']} not found")

            # Move the node to the new parent and adjust tree values
            await self._move_node(current_node, new_parent)

        # Commit changes
        await self.session.commit()

    async def _move_node(self, node: Model, new_parent: Model) -> None:
        """Move a node to a new parent and adjust the tree"""
        old_lft, old_rgt = node.lft, node.rgt
        old_parent_id = node.parent_id

        # Set new parent and update the level
        node.parent_id = new_parent.id
        node.level = new_parent.level + 1
        node.lft = new_parent.rgt
        node.rgt = new_parent.rgt + 1

        # Shift nodes to make space for the moved node
        await self._shift_nodes(node.rgt, 2)

        # Commit the node's new position
        await self.session.commit()

        # Update new parent's rgt value
        new_parent.rgt += 2
        await self.session.commit()

        # Update the previous parent's rgt if needed
        if old_parent_id:
            old_parent = await self.session.get(self.model, old_parent_id)
            if old_parent:
                old_parent.rgt -= 2  # Decrease parent's right value
                await self.session.commit()

    async def _shift_nodes(self, start_rgt: int, shift: int) -> None:
        """Shift all nodes' rgt and lft values to make space for a new node or remove an old one"""
        result = await self.session.execute(select(self.model).filter(self.model.lft >= start_rgt))
        nodes_to_shift = result.scalars().all()

        for node in nodes_to_shift:
            node.lft += shift
            node.rgt += shift

        await self.session.commit()

    async def delete_node(self, node_id: ID) -> None:
        """Delete a node and adjust the tree"""
        node = await self.session.get(self.model, node_id)
        if not node:
            raise ValueError(f"Node with id {node_id} not found")

        # Check if there are any child nodes (nodes with lft/rgt within node's range)
        # result = await self.session.execute(select(model).filter(
        #     model.lft > node.lft, model.rgt < node.rgt))
        result = await self.session.execute(select(self.model).filter(
            self.model.lft.__gt__(node.lft),
            self.model.rgt.__lt__(node.rgt)
        ))
        child_nodes = result.scalars().all()

        # Remove child nodes by shifting the right and left of other nodes
        if child_nodes:
            await self._shift_nodes(node.rgt + 1, -(node.rgt - node.lft + 1))

        # Now remove the node itself
        await self.session.delete(node)
        await self.session.commit()

        # Shift other nodes to fill the gap
        await self._shift_nodes(node.rgt, -(node.rgt - node.lft + 1))

        # Update the parent's rgt value (if it exists)
        if node.parent_id:
            parent = await self.session.get(self.model, node.parent_id)
            if parent:
                parent.rgt -= (node.rgt - node.lft + 1)
                await self.session.commit()

    async def validate_no_cycles(self, node_id: ID, parent_id: ID) -> None:
        """Ensure there are no cyclic references in the hierarchy."""
        current_parent_id = parent_id
        while current_parent_id is not None:
            if current_parent_id == node_id:
                raise ValueError("Cyclic reference detected in the hierarchy.")
            current_parent = await self.session.get(self.model, current_parent_id)
            if current_parent is None:
                break
            current_parent_id = current_parent.parent_id
