# 1. Introduction

This is a detailed description of the demo Web Interface.

:exclamation: Make sure you've read the [Installation & Configuration](https://github.com/comptech-winter-school/coal-composition-control/tree/doc#installation--configuration) section before you start :exclamation:.

# 2. Getting Started

Provided you've successfully connected to the demo host, you should see the following page:

![start](../diagrams/ug/evraz_demo_page.png)

## 2.1 Page Selection

The _EVRAZ fractions demo page_ option in the _page_ combobox must be selected:

![page](../diagrams/ug/evraz_demo_page_selection.png)

## 2.2 Configuration

### 2.2.1 Video Selection

To choose a video to be processed interract with the _video_ combobox:

![Video selection](../diagrams/ug/evraz_demo_video.png)

### 2.2.2 Model Selection

To choose a model to be used in the inference stage interract with the _model_ combobox:

![Model selection](../diagrams/ug/evraz_demo_model.png)

### 2.2.3 Mode Selection

There are two analysis modes available:

- Single frame
- Video

_Single frame_ mode means that the histogram is being cleared every time a new frame comes.
_Video_ mode means that the histogram is not cleared during the whole video accumulating the results.

To select either mode use the _mode_ checkbox (checked means _video_):

![Mode selection](../diagrams/ug/evraz_demo_update.png)

## 2.3 Processing

After you've done with the configuration stage you can start video processing by clicking the _start_ button:

![Start processing](../diagrams/ug/evraz_demo_start.png)

After that you should see new 2 subwindows:

- Processed video window
- Histogram window

### 2.3.1 Processed Video Window

This window plays the selected video (see [Video Selection](#video-selection)) with the results of the object detection
algorithm added:

![Processed video](../diagrams/ug/evraz_demo_rcnn.png)

### 2.3.2 Histogram

This window displays the CDF (cumulative distribution function) of the size of the detected coal pieces:

![Just histo](../diagrams/ug/evraz_demo_just_histo.png)

Hover the mouse cursor over the histogram to display the details:

![Just histo](../diagrams/ug/evraz_demo_histo.png)

The green dashed line is the _cut-line_ - the maximum allowed fraction size when grinding may be skipped.

# 3. References

1. [CDF](https://en.wikipedia.org/wiki/Cumulative_distribution_function)
2. [README.md](https://github.com/comptech-winter-school/coal-composition-control/blob/doc/README.md)
