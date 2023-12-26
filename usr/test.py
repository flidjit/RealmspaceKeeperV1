


"""
startup --
1).    instantiate self.pin_images in self.pin_paths.
2).    instantiate OverworldPins in OverworldMap.location_pins.

ctrl+left_click --
1).    check to see if there is a pin around here.
2-a).    if not, place a new pin.
2-b).    if so, tell the user there is already a pin here.

add_new_pin --
1-a).    a new pin gets an instance_key based on x&y of screen
         click + AltVP.offset. ex. '(100, 100)'.
1-b).    a new pin gets an image_key which references
         a path string in AltVP.pin_paths[image_key].
1-c).    a new pin gets a pin_location & pin_bounding_box based
         on screen_click.
2).    add the new pin to the map.location_pins with instance_key.
3).    add an instance of the pin's pin_images[image_key], to the
       AltVP.pin_instances with instance_key.

"""