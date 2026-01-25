"""
Multithreaded Sorting System - Simple Procedural Implementation
Uses QuickSort for efficient O(n log n) average time complexity.
Two threads sort halves, one thread merges results with proper synchronization.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import random
import time


class SortingSystem:
    """Manages the multithreaded sorting operation."""
    
    def __init__(self):
        self.data_list = []
        self.sorted_list = []
        self.left_half = []
        self.right_half = []
        self.thread_left = None
        self.thread_right = None
        self.thread_merge = None
        self.lock = threading.Lock()
        self.status_log = []
    
    def log_status(self, message):
        """Record status message with timestamp."""
        with self.lock:
            timestamp = time.time()
            self.status_log.append(f"[{len(self.status_log)+1}] {message}")
    
    def validate_input(self, input_string):
        """Validate user input and convert to list of integers."""
        try:
            if not input_string.strip():
                return None, "Input cannot be empty"
            
            # Split by comma or space
            values = input_string.replace(',', ' ').split()
            int_list = [int(val) for val in values]
            
            if len(int_list) < 2:
                return None, "Please enter at least 2 integers"
            
            return int_list, None
        except ValueError:
            return None, "Invalid input: all values must be integers"
    
    def quicksort(self, arr, low, high):
        """
        QuickSort implementation for efficient sorting.
        Time Complexity: O(n log n) average case
        Partition using Lomuto scheme.
        """
        if low < high:
            # Partition and get pivot index
            pivot_index = self._partition(arr, low, high)
            
            # Recursively sort left and right subarrays
            self.quicksort(arr, low, pivot_index - 1)
            self.quicksort(arr, pivot_index + 1, high)
    
    def _partition(self, arr, low, high):
        """Partition array for QuickSort (Lomuto partition scheme)."""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def sort_left_half(self):
        """Thread function: Sort left half of the array."""
        self.log_status("Left thread: Sorting started")
        try:
            self.quicksort(self.left_half, 0, len(self.left_half) - 1)
            self.log_status(f"Left thread: Completed. Sorted: {self.left_half}")
        except Exception as e:
            self.log_status(f"Left thread: ERROR - {str(e)}")
    
    def sort_right_half(self):
        """Thread function: Sort right half of the array."""
        self.log_status("Right thread: Sorting started")
        try:
            self.quicksort(self.right_half, 0, len(self.right_half) - 1)
            self.log_status(f"Right thread: Completed. Sorted: {self.right_half}")
        except Exception as e:
            self.log_status(f"Right thread: ERROR - {str(e)}")
    
    def merge_sorted_halves(self):
        """
        Thread function: Merge two sorted halves.
        This thread waits for both sorting threads to complete using .join().
        """
        self.log_status("Merge thread: Waiting for sorting threads to complete...")
        
        # Wait for both sorting threads to finish
        self.thread_left.join()
        self.thread_right.join()
        
        self.log_status("Merge thread: Both threads completed, starting merge...")
        
        # Merge two sorted arrays
        i, j = 0, 0
        merged = []
        
        while i < len(self.left_half) and j < len(self.right_half):
            if self.left_half[i] <= self.right_half[j]:
                merged.append(self.left_half[i])
                i += 1
            else:
                merged.append(self.right_half[j])
                j += 1
        
        # Add remaining elements
        merged.extend(self.left_half[i:])
        merged.extend(self.right_half[j:])
        
        with self.lock:
            self.sorted_list = merged
        
        self.log_status(f"Merge thread: Completed. Final result: {self.sorted_list}")
    
    def start_sorting(self, data):
        """Start the multithreaded sorting process."""
        self.data_list = data
        self.status_log = []
        self.sorted_list = []
        
        # Divide data into two halves
        mid = len(data) // 2
        self.left_half = data[:mid].copy()
        self.right_half = data[mid:].copy()
        
        self.log_status(f"Starting sort process. Total elements: {len(data)}")
        self.log_status(f"Left half: {self.left_half} (elements: {len(self.left_half)})")
        self.log_status(f"Right half: {self.right_half} (elements: {len(self.right_half)})")
        
        # Create threads
        self.thread_left = threading.Thread(target=self.sort_left_half, daemon=False)
        self.thread_right = threading.Thread(target=self.sort_right_half, daemon=False)
        self.thread_merge = threading.Thread(target=self.merge_sorted_halves, daemon=False)
        
        # Start threads (merge thread waits for others)
        self.thread_left.start()
        self.thread_right.start()
        self.thread_merge.start()
    
    def wait_for_completion(self):
        """Wait for all threads to complete."""
        if self.thread_merge:
            self.thread_merge.join()
        return self.sorted_list


class SortingGUI:
    """GUI for the multithreaded sorting system."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multithreaded Sorting System")
        self.root.geometry("900x700")
        
        self.sorting_system = SortingSystem()
        self.sorting_in_progress = False
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="Multithreaded QuickSort System", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=(0, 15))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Data", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Enter integers (comma or space separated):").pack(anchor=tk.W)
        
        self.input_text = tk.Text(input_frame, height=3, width=80)
        self.input_text.pack(fill=tk.X, pady=(5, 10))
        
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Sort", command=self._on_sort_click).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="Generate Random (20 elements)", 
                   command=self._on_random_click).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="Clear", command=self._on_clear_click).pack(side=tk.LEFT, padx=3)
        
        # Status/Log section
        log_frame = ttk.LabelFrame(main_frame, text="Thread Status Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar for log
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=10, width=100, yscrollcommand=scrollbar.set)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(results_frame, text="Original List:").pack(anchor=tk.W)
        self.original_var = tk.StringVar(value="(Click 'Sort' to start)")
        ttk.Label(results_frame, textvariable=self.original_var, font=("Courier", 10)).pack(anchor=tk.W)
        
        ttk.Label(results_frame, text="Sorted List:").pack(anchor=tk.W, pady=(10, 0))
        self.sorted_var = tk.StringVar(value="(Waiting for results)")
        ttk.Label(results_frame, textvariable=self.sorted_var, font=("Courier", 10), 
                 foreground="green").pack(anchor=tk.W)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def _on_sort_click(self):
        """Handle sort button click."""
        if self.sorting_in_progress:
            messagebox.showwarning("Warning", "Sorting already in progress")
            return
        
        input_str = self.input_text.get()
        data, error = self.sorting_system.validate_input(input_str)
        
        if error:
            messagebox.showerror("Input Error", error)
            return
        
        self.sorting_in_progress = True
        self.log_text.delete(1.0, tk.END)
        self.status_var.set("Sorting in progress...")
        
        self.original_var.set(str(data))
        self.sorted_var.set("(Sorting...)")
        
        # Start sorting in a separate thread to prevent GUI freeze
        sorting_thread = threading.Thread(target=self._perform_sort, args=(data,), daemon=False)
        sorting_thread.start()
    
    def _perform_sort(self, data):
        """Perform sorting and update UI."""
        try:
            self.sorting_system.start_sorting(data)
            result = self.sorting_system.wait_for_completion()
            
            # Update UI
            self.sorted_var.set(str(result))
            
            # Update log
            for log_entry in self.sorting_system.status_log:
                self.log_text.insert(tk.END, log_entry + "\n")
            
            self.status_var.set("Sorting completed successfully!")
            messagebox.showinfo("Success", "Sorting completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Sorting failed: {str(e)}")
            self.status_var.set("Error during sorting")
        finally:
            self.sorting_in_progress = False
    
    def _on_random_click(self):
        """Generate random list."""
        random_list = [random.randint(1, 100) for _ in range(20)]
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, " ".join(map(str, random_list)))
        self.status_var.set("Random list generated (20 elements)")
    
    def _on_clear_click(self):
        """Clear input."""
        self.input_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.original_var.set("")
        self.sorted_var.set("(Waiting for results)")
        self.status_var.set("Ready")


if __name__ == "__main__":
    root = tk.Tk()
    gui = SortingGUI(root)
    root.mainloop()
