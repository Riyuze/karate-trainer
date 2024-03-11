# Karate Trainer #
A pose similarity project which measures how accurate a specific karate move is.
This project was made using **Python** and utilizing several tools and frameworks such as **YoloV5**, **MediaPipe**, **Tensorflow**, and **TKinter**.

# Pre-requisites #
Create a python virtual environment using:
```bash
python -m venv /path/to/new/virtual/environment
```

Then, fork the code and place it in the root folder.

Next, activate the virtual environment using (Windows):
```bash
Scripts/activate
```

Check https://docs.python.org/3/library/venv.html for more details.

After the virtual environment is activated, install the dependencies needed using:

```bash
pip install -r requirements.txt
```

# How to Run #
1. Run karate_trainer.py
   
   ```bash
    py karate_trainer.py
   ```
2. Press **Start** on the homescreen to pick a training plan.
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/3b91e0dc-48d0-42a6-84cf-75c52a3ab7d8)
3. After picking a training plan, click **Start** to start training.
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/63c1c839-35fb-4931-ac4b-64a609d002a9)
3. Pick your video capture device, and press **Show Camera**.
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/eb663338-be2a-4c6f-9ca1-5d2980fe6f66)
4. This will open up a window showing your camera, and press **Space** on your keyboard to start training.
5. Timer will start counting down, images will be captured when timer hits 0 and a double beep sound is played.
6. After training is finished, you can press **Space** again to restart training, or **Escape** to stop training.
7. After stopping training, press the **Preview** button to see the captured images.
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/26c716ef-2e01-425d-9ccf-f4a239e4c36e)
8. Press the **Get Image** button to retrieve the pictures.
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/0c61a1a8-0f83-4cf0-8410-3dd54a16ef08)
9. If the images are satisfactory, press the **Process** button to start processing the image.
10. After the processing is finsihed, result of how accurate the moves are will be shown.
    ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/7601fd8f-ea05-401f-83d6-6b9866d1016c)

# How it Works #
1. Images captured by the camera are first cropped utilizing an object detection model.
   The model will return a box coordinate of where the subject is in the picture and by using slicing, the picture is cropped.
   
   Before:
   
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/10322ebe-115f-4f2d-8966-5a7c31bc2190)
   
   After:
   
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/b2c5e971-eeca-4d93-86f9-a79ae550037a)

2. These cropped images are then processed by MediaPipe to get **X**, **Y**, **Z**, and **Visibility** values from 33 keypoints in the target's body.
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/3092ef60-22b3-4e33-86b2-8a2330e9b72b)
3. These values are then passed into the calculation function to calculate how similar these values are compared to the reference target.
4. These values are also used to plot a 3D skeletal figure which can be rotated.
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/bf73cee8-5e14-47ce-bf50-be512f587d17)
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/7580ff32-61c9-43ce-bfe9-aea76e119241)
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/6219df08-b95e-4bce-97d5-6144955cb5b1)
   ![image](https://github.com/Riyuze/karate-trainer/assets/98701660/a66cfe33-be54-40c5-bd37-ddf9edad5254)
