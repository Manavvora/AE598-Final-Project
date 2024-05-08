import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import json
import matplotlib.colors as mcolors

# Load the sfm_data.json file
with open('results_cam/reconstruction_sequential/sfm_data.json', 'r') as f:
    sfm_data = json.load(f)

# Initialize lists to store rotation matrices and translation vectors (centers)
rotations = []
translations = []
keys = []
# Extract rotations and translations from extrinsics and identify the origin camera
origin_rotation = None
origin_translation = None

for camera_pose in sfm_data.get("extrinsics", []):
    key = camera_pose["key"]
    print(f'Camera {key}')
    rotation = np.array(camera_pose["value"]["rotation"])
    center = np.array(camera_pose["value"]["center"])
    if key == 0:
        origin_rotation = rotation
        origin_translation = center
    rotations.append(rotation)
    translations.append(center)
    keys.append(key)

# Compute the inverse transformation of the origin camera
if origin_rotation is not None and origin_translation is not None:
    print("Origin camera found")
    inv_rotation = np.transpose(origin_rotation)  # Inverse of a rotation matrix is its transpose
    inv_translation = -inv_rotation @ origin_translation  # Transform the center

# Apply the inverse transformation to all cameras
transformed_positions = []
transformed_orientations = []
for R, t in zip(rotations, translations):
    transformed_R = inv_rotation @ R
    transformed_t = inv_rotation @ t + inv_translation
    transformed_positions.append(transformed_t)
    transformed_orientations.append(transformed_R)

cmap = plt.get_cmap('viridis')
norm = mcolors.Normalize(vmin=min(keys), vmax=max(keys))

# Function to plot camera poses
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# For each camera, plot the camera position and orientation
for key, R, t in zip(keys, transformed_orientations, transformed_positions):
    # Compute camera orientation in order to plot the camera axes
    cam_orientation = R.T
    cam_position = -R.T @ t  # Convert from OpenMVG format to standard format

    # Define the length of the camera axes (can be adjusted for better visualization)
    axis_length = 0.1  # Adjusted for better visibility

    # Determine the color
    color = cmap(norm(key))

    # Special marking for the origin camera
    if key == 0:
        marker = '^'  # Triangle marker for the origin camera
        label = f'Origin Camera {key}'
        size = 100  # Larger size for the origin
    else:
        marker = 'o'
        label = f'Camera {key}'
        size = 50  # Smaller size for other cameras

    # Plot camera position
    ax.scatter(cam_position[0], cam_position[1], cam_position[2], color=color, s=size, marker=marker, label=label)

    # Plot camera axes
    for i in range(3):
        ax.quiver(
            cam_position[0], cam_position[1], cam_position[2],
            cam_orientation[i, 0], cam_orientation[i, 1], cam_orientation[i, 2],
            length=axis_length, normalize=True, color=color
        )

# Set axes labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set title
ax.set_title('Camera Poses')

# Adjust the legend
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

# Show the plot
plt.show()