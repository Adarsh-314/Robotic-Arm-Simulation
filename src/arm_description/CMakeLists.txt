cmake_minimum_required(VERSION 3.8)
project(arm_description)

find_package(ament_cmake REQUIRED)

# Install resource directories
install(DIRECTORY
  urdf
  config
  launch
  DESTINATION share/${PROJECT_NAME}/
)

# Install Python script
install(PROGRAMS
  scripts/arm_controller.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()