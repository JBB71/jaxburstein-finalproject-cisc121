# jaxburstein-finalproject-cisc121

# Algorithm - Quick Sort
This program is an user friendly and interactive app that teaches people what the main idea of a quick sort algorithm is. Instead of the program just sorting a list or array by itself, the user chooses which numbers are greater, equal, or less than the chosen pivot. The program will give feedback, show the correct partitions for the user to be able to learn from their mistakes, and helps the user until the list/array is fully sorted. 
## Problem Breakdown & Computational Thinking (You can add a flowchart and write the four pillars of computational thinking briefly in bullets)
Decomposition:
 - Take in a random list of elements
 - Choose a pivot point at random
 - Ask the user whether a number in the unsorted array is part of the left (less than) or right (greater than) partition
 - If the user is correct then tell them and append their choice into the new list
 - If user is wrong tell them why and tell them to try again
 - Display the final sorted list and tell user how accurate they were

Pattern Recognition:
 - Select pivots each time
 - Compare elements to the pivot
 - Partition into left and right subarrays

Abstraction:
 - To not overwhelm the user:
   - Only display the pivot and one element
   - Only offer left or right as an option for the user
 
![IMG_0077](https://github.com/user-attachments/assets/58bdfd06-0449-4730-b063-5eb4b9b6b4cb)


## Steps to Run
1. Choose whether you want the pivot to be the first middle or random element of the list
2. Generate list
3. Look at what the pivot value is
4. Look at what the current element is
5. Choose whether the current element is either greater or less than the pivot element by choosing left partition or right partition
6. Pick left or right until final array is sorted
<img width="1413" height="655" alt="Screenshot 2025-11-29 at 11 53 27 AM" src="https://github.com/user-attachments/assets/5a524c46-7fbc-4c16-b48d-98d530231992" />
<img width="1424" height="669" alt="Screenshot 2025-12-06 at 6 19 47 PM" src="https://github.com/user-attachments/assets/357ad63e-75d5-427b-bc44-6039c90e1e4e" />
<img width="1438" height="682" alt="Screenshot 2025-12-06 at 6 19 58 PM" src="https://github.com/user-attachments/assets/de822b6b-fcec-4ef2-bc87-c10dd86406e4" />
<img width="1438" height="680" alt="Screenshot 2025-12-06 at 6 21 07 PM" src="https://github.com/user-attachments/assets/92405b67-ce69-4c3c-9d98-4e23b1698b07" />
<img width="1436" height="759" alt="Screenshot 2025-12-06 at 6 21 21 PM" src="https://github.com/user-attachments/assets/7de929e6-b77d-411f-b454-8e17b390aad9" />

## Hugging Face Link
https://huggingface.co/spaces/JBB71/CISC121-FinalProject/tree/main
## Author & Acknowledgment
Jax Burstein
CISC 121 — Final Project
Queen’s University
Acknowledgment: Gradio for its library ChatGPT for assistance with debugging and documentation
