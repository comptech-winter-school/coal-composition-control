# 1. Introduction

This is a detailed description of a demo interface.

# 2. Getting Started

Provided you've successfully connected to the demo host, you should see the following page:

![start](../diagrams/ug/evraz_demo_page.png)

## 2.1 Page Selection

The `EVRAZ fractions demo page` option in the `Page` combobox must be selected:

![page](../diagrams/ug/evraz_demo_page_selection.png)

## 2.2 Configuration

### 2.2.1 Video Selection

To choose a video to be processed interract with the _video_ combobox:

![Video selection](../diagrams/ug/evraz_demo_video.png)

### 2.2.2 Model Selection

To choose a model to be used in the inference stage interract with the _model_ combobox:

![Model selection](../diagrams/ug/evraz_demo_model.png)

### 2.2.3 Mode Selection

There are two analysis modes:

- Updating
- Non-updating

_Updating_ mode means that the histogram updates each frame, i.e. it is cleared each time a new frame is processed.
_Non-updating_ mode means that the histogram is not cleared

To select either mode use the `mode` checkbox:

![Mode selection](../diagrams/ug/evraz_demo_update.png)

### 2.2.4 Start Processing

After you've done with the configuration stage you can start video processing by clicking the `start` button:

![Start processing](../diagrams/ug/evraz_demo_start.png)

## 2.3 Display

![page](../diagrams/ug/evraz_demo_histo.png)
