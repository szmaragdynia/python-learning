#nie ma takiego modulu xD



# Import the RoomSketcher module
import roomsketcher as rs

# Create a new project
project = rs.Project("My Room")

# Draw the floor plan
floor_plan = rs.FloorPlan(project)
floor_plan.draw_polygon([(0, 0), (0, 4), (1.5, 4), (1.5, 5), (3.5, 5), (3.5, 4), (5, 4), (5, 0)]) # Draw a polygon for the room shape
floor_plan.add_door(0, 2, "left") # Add a door on the left wall at 2m from the bottom
floor_plan.add_window(3.5, 5, "top") # Add a window on the top wall at 3.5m from the left

# Add fixtures and furniture
furniture = rs.Furniture(project)
furniture.add_sofa(1.5, 2.5, "right") # Add a sofa at 1.5m from the left and 2.5m from the bottom, facing the right wall
furniture.add_coffee_table(2.5, 2.5, "center") # Add a coffee table at 2.5m from the left and 2.5m from the bottom, centered in the room
furniture.add_tv(3.75, 4, "bottom") # Add a TV at 3.75m from the left and 4m from the bottom, facing the bottom wall
furniture.add_desk(4.25, 1.25, "left") # Add a desk at 4.25m from the left and 1.25m from the bottom, facing the left wall
furniture.add_chair(4.25, 0.75, "left") # Add a chair at 4.25m from the left and 0.75m from the bottom, facing the left wall
furniture.add_bookcase(3.75, 0, "top") # Add a bookcase at 3.75m from the left and 0m from the bottom, facing the top wall

# Save the project as a file for RoomSketcher
project.save("my_room.rsk")