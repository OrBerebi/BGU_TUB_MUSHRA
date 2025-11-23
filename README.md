# BGU TUB MUSHRA Experiment

This document provides instructions for running the MUSHRA listening test experiment.

## 🚀 User Guide

This guide will walk you through setting up and running the MUSHRA experiment on your computer.

---

### 1. Get the Project Files (Clone the Repository)

Before you can install any software, you need to get the project files onto your computer. We'll use GitHub Desktop, which makes this easy.

1. **Install GitHub Desktop (if you don't have it):**

   * Go to the official website: <https://desktop.github.com/>

   * Download and install the application for macOS.

   * Open the app and log in with your GitHub account.

2. **Clone the Repository:**

   * Navigate to this project's main page on GitHub.

   * Click the green **`< > Code`** button.

   * In the dropdown menu, click on **"Open with GitHub Desktop"**.

   * Your browser will ask for permission to open the GitHub Desktop app. Allow it.

   * The app will open and ask you where you want to save the project (the "Local Path").

   * **Choose a simple location you can remember**, like `Documents/GitHub/BGU_TUB_MUSHRA`.

   * Click the **"Clone"** button.

All the project files, including the `start_experiment.sh` and `environment.yml` files, are now on your computer in that folder.


### 2. Install Pure Data (Pd)

This experiment relies on a specific version of Pure Data (Pd) to handle the audio. You must install version **0.55-0**.

1.  **Download:** Go to the official Pure Data downloads page: `https://puredata.info/downloads/pure-data/releases/0.55`
2.  **Install:**
    * Open the `.dmg` file you downloaded.
    * Drag the `Pd-0.55-0.app` icon directly into your main **Applications** folder.

> **⚠️ Critical Requirement**
>
> * You **must** install the app in your main `/Applications` folder.
> * Do **not** rename the app. It must be named exactly `Pd-0.55-0.app`.
>
> The experiment's start script (`start_experiment.sh`) has this *exact* file path hard-coded. If you install it anywhere else or rename it, the experiment will fail to launch.

---

### 3. Set Up the Python Environment

This project uses a specific set of Python libraries. The easiest way to manage these is by using Anaconda and the provided environment file.

1.  **Install Anaconda (if you don't have it):**
    * If you don't already have Anaconda or Miniconda, go to the [Anaconda download page](https://www.anaconda.com/download) and install the macOS version.
    * Follow the on-screen instructions from the installer.

2.  **Navigate to the Project Directory:**
    * Open your **Terminal** (you can find it using Spotlight: ⌘ + Space, then type "Terminal").
    * Use the `cd` (change directory) command to move into the folder where you cloned or downloaded this project (the folder that contains the `environment.yml` file).
    * **Example:**
        ```bash
        cd ~/Documents/GitHub/BGU_TUB_MUSHRA
        ```

3.  **Create the Conda Environment:**
    * Run the following command in your terminal. This will read the `environment.yml` file, create a new environment, and automatically install all the correct library versions.
        ```bash
        conda env create -f environment.yml
        ```
    * This step might take a few minutes as it downloads and installs the packages.

4.  **Activate the Environment:**
    * Once the environment is created, you must **activate** it. The environment's name is specified inside the `environment.yml` file (look for the `name:` line at the top).
    * Assuming the name is `bgu_tub_mushra`, you would run:
        ```bash
        conda activate bgu_tub_mushra
        ```

> **IMPORTANT:**
>
> You must **always** activate this environment (`conda activate bgu_tub_mushra`) every time you open a new terminal window to run the experiment.
>
> You'll know it's active because your terminal prompt will change to show `(bgu_tub_mushra)` at the beginning.

### 4. Run the Experiment

Now that everything is installed and set up, you are ready to run the experiment.

1. **Open your Terminal.**

2. **Activate the Conda Environment** (if it's not already active):
   ```bash
    conda activate bgu_tub_mushra
    ```
3. **Navigate to the Project Directory** (if you're not already there):
   ```bash
    cd ~/Documents/GitHub/BGU_TUB_MUSHRA
    ```
4. **Run the Start Script:**

* The first time you run this, you might need to make the script "executable." Run this command just once to be safe (it won't hurt to run it more than once):

  ```
  chmod +x start_experiment.sh
  
  ```

* Now, run the experiment:

  ```
  ./start_experiment.sh
  
  ```

That's it! This will launch both the Pure Data audio engine in the background and the main Python GUI for the experiment.

When you finish the experiment your ratings will be saved at `/bgu_results/`
