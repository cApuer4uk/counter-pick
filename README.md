# YOLO Training (Dota 2 Heroes)

The trained model is later used inside the Counterpick overlay application.

## Virtual environment (optional)
https://drive.google.com/file/d/1YQo469v3SmAb_Ag_V2u62czV8jnA-XGA/view

## Project structure

```
counterpick/ # project root
│
├─ .venv/ # python virtual environment
│
├─ counterpick/ # main package folder
│ │
│ ├─ ml/ # YOLO workspace
│ │ ├─ images/ # dataset images
│ │ ├─ labels/ # YOLO labels
│ │ │
│ │ ├─ runs/ # training outputs
│ │ │ └─ detect/ # detection runs
│ │ │ └─ train/ # latest training run
│ │ │ └─ weights/ # trained weights
│ │ │ ├─ best.pt # best model
│ │ │ └─ last.pt # last checkpoint
│ │ │
│ │ ├─ all_labels.txt # class list
│ │ ├─ botsort.yaml # tracker config
│ │ ├─ data.yaml # dataset config
│ │ └─ yolo_train_start.py # training launcher
│ │
│ └─ scripts_for_help/ # helper scripts
│ ├─ datayaml_generate.py # generate data.yaml
│ ├─ ml_check.py # inference test
│ ├─ screenshot_detector.py # detector helper
│ └─ yolov8m.pt # MAIN base model (used for training)

```