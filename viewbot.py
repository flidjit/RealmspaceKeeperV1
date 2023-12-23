import tkinter as tk
from panda3d.core import NodePath, TextureStage
from direct.showbase.ShowBase import ShowBase

from default.altviewports.newoverworld_altvp import OverworldMapAltVP
from default.datatypes import OverworldMapData, ModelData, TileData, BeingData
from default.altviewports.startup_altvp import StartupAltVP


class ViewBot:
    """ ViewBot Portfolio:
    -    Saves/Loads/Handles GameMapData and ModelData.
    -    Contains a viewport used to display 3-d objects.
    -    Contains an alt-viewport used to display tkinter windows.
    -    Draws the given 3-d map.
    -    Makes changes to the map object."""

    def __init__(self, mother=None):
        self.mother = mother
        self.viewport = tk.Frame(
            self.mother.mother_frame, bg='red')
        self.viewport.place(
            x=15, y=55, width=800, height=400)
        self.alt_viewport = StartupAltVP(
            self.mother.mother_frame, mother=self.mother)
        self.map_data = None
        self.models = {}
        self.textures = {}
        self.cam = None
        self.cursor_3D = None

    def load_model(self, tile=None, being=None):
        """
        Load a model based on the provided Tile or Being.

        Parameters:
        - tile (Tile): The Tile object representing the model to be loaded.
        - being (Being): The Being object representing the model to be loaded.
        """
        if tile:
            model_path = tile.model_path
            position = (tile.x, tile.y, tile.z)
        elif being:
            model_path = being.model_path
            position = (being.x, being.y, being.z)
        else:
            return

        if model_path not in self.models:
            model = self.mother.loader.load_model(model_path)
            if not model:
                print(f"Failed to load model: {model_path}")
                return
            node_path = NodePath(model)
            node_path.set_pos(*position)
            node_path.reparent_to(self.mother.render)
            self.models[model_path] = node_path

    def swap_texture(self, model, texture_path):
        if texture_path in self.textures:
            texture = self.textures[texture_path]
        else:
            texture = self.mother.loader.load_texture(texture_path)
            if not texture:
                print(f"Failed to load texture: {texture_path}")
                return
            self.textures[texture_path] = texture
        texture_stage = TextureStage("texture_stage")
        model.set_texture(texture_stage, texture)

    def load_map(self, map_data):
        print('load the stage')

    def show_overworld_map(self, overworld_map_data=None):
        if overworld_map_data:
            self.alt_viewport = OverworldMapAltVP(
                master=self.mother.root,
                overworld_map=overworld_map_data)

    def unload_model(self, node_path):
        """
        Unload a model represented by the provided NodePath.

        Parameters:
        - node_path (NodePath): The NodePath representing the model to be unloaded.
        """
        if not node_path:
            return

        # Detach the NodePath from the scene graph
        node_path.detach_node()

        # Remove the model from the dictionary if it was loaded
        for model_path, loaded_node_path in list(self.models.items()):
            if loaded_node_path == node_path:
                del self.models[model_path]

        # Release the resources associated with the NodePath
        node_path.remove_node()

    def get_tile_by_position(self, position):
        """
        Get the tile at the specified position.

        Parameters:
        - position (tuple): The (x, y) coordinates of the tile.

        Returns:
        - Tile or None: The Tile object at the specified position or None if not found.
        """
        # Iterate through all chunks in the map data
        for chunk_coordinates, chunk in self.map_data.chunks.items():
            # Check if the specified position exists in the chunk
            if position in chunk.tiles:
                return chunk.tiles[position]

        # If the tile is not found in any chunk, return None
        return None

    def add_tile(self, chunk_id, x, y, z, model_path):
        """
        Add a new tile to the specified chunk.

        Parameters:
        - chunk_id (str): The ID of the chunk where the tile will be added.
        - x (float): The x-coordinate of the tile's position.
        - y (float): The y-coordinate of the tile's position.
        - z (float): The z-coordinate of the tile's position.
        - model_path (str): The file path to the 3D model for the tile.
        """
        # Check if the chunk exists in the dictionary
        if chunk_id not in self.map_data.chunks:
            self.map_data.chunks[chunk_id] = ChunkData(map_data={})

        # Create a new Tile object
        new_tile = TileData(
            model_path=model_path, render=self.mother.render,
            x=x, y=y, z=z)

        # Add the tile to the chunk
        tile_id = (x, y)
        self.map_data.chunks[chunk_id].tiles[tile_id] = new_tile

        # Load the model associated with the tile
        self.load_model(tile=new_tile)

    def add_occupant(self, chunk_id, occupant_id,
                     x, y, z, model_path):
        """
        Add a new occupant to the specified chunk.

        Parameters:
        - chunk_id (str): The ID of the chunk where the occupant will be added.
        - occupant_id (str): The ID of the occupant.
        - x (float): The x-coordinate of the occupant's position.
        - y (float): The y-coordinate of the occupant's position.
        - z (float): The z-coordinate of the occupant's position.
        - model_path (str): The file path to the 3D model for the occupant.
        """
        # Check if the chunk exists in the dictionary
        if chunk_id not in self.map_data.chunks:
            self.map_data.chunks[chunk_id] = ChunkData(map_data={})

        # Create a new Being object
        new_occupant = BeingData(model_path=model_path,
                                 render=self.mother.render,
                                 x=x, y=y, z=z)

        # Add the occupant to the chunk
        occupant_id = occupant_id
        self.map_data.chunks[chunk_id].occupants[occupant_id] = new_occupant

        # Load the model associated with the occupant
        self.load_model(being=new_occupant)

    def delete_tile(self, chunk_id, tile_id):
        """
        Delete an existing tile from the specified chunk.

        Parameters:
        - chunk_id (str): The ID of the chunk where the tile exists.
        - tile_id (tuple): The ID of the tile (e.g., (x, y)).
        """
        # Check if the chunk exists in the dictionary
        if chunk_id in self.map_data.chunks and tile_id in self.map_data.chunks[chunk_id].tiles:
            # Get the tile from the chunk
            tile = self.map_data.chunks[chunk_id].tiles[tile_id]

            # Unload the model associated with the tile
            self.unload_model(tile.node_path)

            # Remove the tile from the chunk
            del self.map_data.chunks[chunk_id].tiles[tile_id]

    def delete_occupant(self, chunk_id, occupant_id):
        """
        Delete an existing occupant from the specified chunk.

        Parameters:
        - chunk_id (str): The ID of the chunk where the occupant exists.
        - occupant_id (str): The ID of the occupant.
        """
        # Check if the chunk exists in the dictionary
        if chunk_id in self.map_data.chunks and occupant_id in self.map_data.chunks[chunk_id].occupants:
            # Get the occupant from the chunk
            occupant = self.map_data.chunks[chunk_id].occupants[occupant_id]

            # Unload the model associated with the occupant
            self.unload_model(occupant.node_path)

            # Remove the occupant from the chunk
            del self.map_data.chunks[chunk_id].occupants[occupant_id]

    def update(self):
        # Perform any necessary updates in the stage
        pass

