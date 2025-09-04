Real-Time Static Hand Gesture Recognition

Name: Jinix Chacko

Technology Justification

I chose MediaPipe Hands for hand detection and landmark extraction and OpenCV for real-time video processing.

MediaPipe: This framework provides a pre-trained, highly accurate, and performant model for detecting 21 key hand landmarks. It is the ideal choice for this project as it eliminates the need to build and train a custom hand detection model from scratch, allowing for robust real-time performance on a live video stream. Its output of landmark coordinates is perfectly suited for a rules-based gesture recognition system.

OpenCV: This is the standard for computer vision tasks in Python. It provides the necessary tools for capturing video from a webcam, displaying the video feed in a window, and drawing visual elements like bounding boxes and text overlays.

Gesture Logic Explanation

The gesture recognition is based on a rules-based algorithm that analyzes the relative positions of the finger landmarks provided by MediaPipe. I determined the state of each of the five fingers (open or closed) by comparing the Y-coordinate of each finger's tip landmark to the Y-coordinate of a key joint at the base of the finger.

For example:

    Open Palm: All five fingers have their tip landmarks above their respective base joints.

    Fist: All five fingers have their tip landmarks below their respective base joints.

    Peace Sign: Only the index and middle finger tips are above their base joints, while the others are below.

    Thumbs Up: The thumb tip is extended upwards, while the other four fingers are closed. A specific check for the thumb's vertical position relative to its base ensures accuracy.

Setup and Execution

    Clone the Repository:
    git clone [your_repo_link]

    Navigate to the Project Directory:
    cd [your_repo_name]

    Create and Activate a Virtual Environment:
    python -m venv venv
    source venv/bin/activate (macOS/Linux) or venv\Scripts\activate (Windows)

    Install Dependencies:
    pip install -r requirements.txt

    Run the Application:
    python main.py