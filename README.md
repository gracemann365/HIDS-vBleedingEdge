# HIDS - Home Intrusion Detection System (Locally vBleedingEdge)

## Overview:

HIDS is a locally deployed Home Intrusion Detection System designed to enhance home security through real-time monitoring and alerting. Leveraging cutting-edge technologies like YOLO (You Only Look Once) object detection and Flask web framework, this system detects intruders and provides immediate notifications to homeowners via email.

## Key Features:

- **Real-time Object Detection:** 
  - Utilizes YOLO object detection model to identify intruders in real-time from webcam footage.
  - Utilizes YOLO (You Only Look Once) object detection model, a state-of-the-art deep learning framework.
    - YOLO employs a single neural network to simultaneously predict bounding boxes and class probabilities.
    - It divides the image into a grid and predicts bounding boxes and probabilities for each grid cell, enabling efficient detection.
    - YOLOv3, the version implemented in HIDS, enhances accuracy and speed by integrating multiple detection scales and advanced feature extraction techniques.
  
- **Email Alerting:**
  - Sends instant email notifications to homeowners upon detecting suspicious activity, enabling rapid response.
    - Utilizes Simple Mail Transfer Protocol (SMTP) for sending emails securely over the internet.
    - Implements two-factor authentication (2FA) architecture of Google Workspace for enhanced email security.
      - Google Workspace 2FA adds an extra layer of protection by requiring users to verify their identity through a secondary method, such as a mobile device or authenticator app.
      - This ensures that only authorized users can access the email alerting system, preventing unauthorized access and enhancing overall system security.

  
## Key Features:

- **Flask Web Interface:**
  - Offers a user-friendly web interface powered by Flask for easy monitoring of detected intrusions and system status.
    - Utilizes the lightweight and flexible architecture of Flask, a micro web framework for Python, to create dynamic web applications.
    - Flask follows a modular design, allowing developers to build scalable and maintainable web interfaces by organizing code into smaller, reusable components.
      - This modular approach enhances performance by reducing overhead and improving code maintainability, resulting in faster response times and better overall user experience.


## Installation:

1. Clone the HIDS repository to your local machine:

    ```bash
    git clone <repository-url>
    ```

2. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure email settings in `config.py` to enable email alerting.

4. Run the application:

    ```bash
    python app.py
    ```

5. Access the web interface at [http://localhost:5000](http://localhost:5000) to monitor intrusions and system status.

## Usage:

- Launch the HIDS system by running `app.py`.
- Navigate to the web interface to view live camera feed and intrusion alerts.
- Receive email notifications upon detecting intruders for immediate action.

## Contributing:

Contributors to HIDS are valued and appreciated! Special thanks to all those who have contributed to this project:

1. David Grace - Tech Lead & Project Manager
2. Adersh S Thomas - Developer (Python)
3. Akshay S P - Developer (UI/UX)
4. Jayasurya - Intern

## Version History:
### v1.0 (Genesis - YOLO Person Detection):
- Initial release featuring basic YOLO person-class detection with Alarm Trigger functionality.
- Capable of distinguishing humans from other animate and inanimate objects.
- Implemented real-time detection and alerting system.

### v2.0 (Enhanced Control Interface - Flask Dashboard):
- Introduced Flask Dashboard Interface.
- Provided clients with initial intruder detection alerts and administrative control.
- Enhanced user experience with interactive controls and customizable settings.

### v3.0 (Advanced Alerting and Classification - SMTP Email Integration):
- Integrated SMTP email alerting system.
- Delivered notifications to client email addresses with precise timestamps.
- Implemented classification of humanoids as daytime humanoids or intruders based on predefined curfew times.
- Enhanced alerting system with customizable email templates and recipient lists.

### v3.5 (Performance Optimization and UI Refinement - Cyberpunk Theme):
- Enhanced overall system performance and responsiveness.
- Revamped user interface with a cyberpunk-themed design.
- Provided a visually appealing and immersive environment for monitoring and control.
- Improved system stability and reliability through optimized code architecture.
- Streamlined user workflows with intuitive navigation and enhanced usability features.

## BleedingEdge Development Model:
- The term "BleedingEdge" denotes the primary development branch.
- It houses the latest updates and experimental features.
- New updates and features are developed as deviations from the BleedingEdge branch, ensuring a continuous cycle of innovation and improvement.

## Disclaimer:

This software is provided as-is and without warranty. Use at your own risk.

## Contact:

For any inquiries or support, please contact [maintainer-email](mailto:gecbhsender@gmail.com).

## License:

This project is licensed under the MIT License - see the LICENSE file for details.

