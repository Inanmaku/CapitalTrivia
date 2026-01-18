  # Capital Trivia

Capital Trivia is a Python-based educational quiz app built with PyQt5, designed to teach world capitals through an engaging chat-style interface that mimics a mobile messaging app. The app combines interactive design, progressive learning, and state persistence to create a polished educational experience.


How It Works:


The app opens in a phone-style, frameless window with a messaging app layout.
Questions appear as chat bubbles on the left side, like a conversation.
Users type their answers as if messaging back, making the experience interactive and natural.
Questions are presented in sets of 20:
If answered correctly on the first try, they won’t be asked again.
Incorrect answers are deferred and repeated until answered correctly.
After completing a set, the app automatically moves to the next set of 20 questions.
Emotes provide feedback based on performance: for example, if a question is answered incorrectly three times, a visual emote is displayed.
Users can access the menu in the top-right corner, then navigate to the editing page:
View all question bubbles.
Open a toolbar to delete or edit questions without losing progress on previously answered questions.
Add new questions by scrolling down and creating new bubbles.
Restart the quiz entirely using the toolbar.
Progress is automatically saved when leaving the editing page.
Closing the app prompts the user to save changes.
Choosing Yes saves progress and edits.
Choosing No restores the app to its original state on next launch.


Key Features:


Set-Based Learning: Reinforces retention by repeating only incorrect answers until mastered.
Chat-Style UX: Engaging, phone-like interface designed to make learning interactive.
Draggable Window: Frameless design lets you move the “phone” interface anywhere on your screen.
Progress Persistence: Tracks which questions were answered correctly and remembers edits or deletions.
Editable Content: Users can add, remove, or modify questions.
Visual Feedback: Emotes reinforce user performance and learning progress.
Experimental UI: Frameless window, chat bubbles, and interactive star elements demonstrate custom PyQt5 UI skills.



Installation


Clone the repository:

git clone https://github.com/inanmaku/capitaltrivia.git
cd capital-trivia


Install dependencies:

pip install PyQt5


Run the app:

python main.py


This project demonstrates:
Custom GUI design with PyQt5, including custom widgets, chat bubbles, and interactive elements.
State management with progress tracking and deferred question logic.
UX design thinking, including set-based repetition, feedback emotes, and natural input methods.
File I/O & persistence, allowing user edits and progress to survive app restarts.
