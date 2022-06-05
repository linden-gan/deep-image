# Deep image
Extract depth information from a pair of stereo images. \
Our final product is an executable that could calculate and display depth information at clicked position using two webcams in real time.

## Motivation & Problem Setup
Depth informaton are sometime useful. We want our images tell us how far an object is instead of just some flat 2D information. This can be crucial in auto-drive, 3D environment reconstruction, and distance measurement. Certainly, there eixist tools like tape measure or LIDAR that can measure depth information. However, with the help of computer vision stereo matching techniques, we can achieve the same thing with equipments that normal people have in their daily life like webcams or cellphone camaras, as long as we have the parameters like distance between two cameras, focal lengths, and correct calibration. With properly desgined setup, we can even output the depth estimation in real time!

We explored both the traditional (stereo box match, graph cut) and neural network solutions for calculating disparity maps, and finally choose traditional stereo box match to achieve real time depth estimation from two webcams.

## Data used
- Photos taken by ourselves
- Kitti stereo dataset
- Middlebury stereo dataset

## Technologies & techniques used
### Traditional (based on opencv, stereo box match)
#### Prereq
- numpy (`pip install numpy`)
- opencv (cv2) (`pip install opencv-python`)
- matplotlib (`pip install matplotlib`)
- gcc compiler (already installed in Linux and Mac, please download MinGW for gcc [here](https://www.mingw-w64.org/))
- hardwares (two cameras, recommended to use two exactly same webcams so that they can be easily connected to computers and produce same-size images)

#### Pipeline & Algorithm
- First, we caliberate our webcams to get rid of distorted margin. Next, we input two stereo images to OpenCV's library function to get a disparity map, which represents shifts of each pair of pixels from left and right images. Then, we compute the depth of each pixel based on its shift. Finally, we output the depth information so that user can know each pixel's depth once they click it.
- 

#### Challenges we ran into


### Neural Network (utilized [MobileStereoNet](https://github.com/cogsys-tuebingen/mobilestereonet))
After exploring the open sourced codebases from the top 100 Kitti stereo dataset benchmark, we choose to test on MobileStereoNet. Specifically for this project, we utlized three versions of pretrained versions of 3D-MobileStereoNet that are trained on (SF only), (SF then finetuned on DS), (SF then finetuned on DS and KITTI2015). (available on the github page for [MobileStereoNet](https://github.com/cogsys-tuebingen/mobilestereonet))

SF: Scene Flow, DS: Driving Stereo

#### Prereq
Follow the readme for [MobileStereoNet](https://github.com/cogsys-tuebingen/mobilestereonet), then used the tweaked version of [prediction.py](neural_network/prediction.py) (credits to the authors of MobileStereoNet), and visualize script written by us [visualize_disparity.py](neural_network/visualize_disparity.py) that converts npz real disparity maps into visible png images.

The command to run the predition is
 ```shell
 python prediction.py --datapath ./ --testlist ./filenames/own_test.txt --loadckpt {YOUR CKPT PATH} --dataset kitti --colored 0 --model MSNet3D
 ```

#### Challenges we ran into
- We originally intended to train our own version of model for a preexisting codebase with different training parameters. However, most open source stereo matching depth estimation codebase are specialized for dataset benchmarks and don't have many options to tweak the training parameters.
- In addition, the huge number of training data from datasets like Scene Flow, Driving Stereo, and Kitti would be extremely time consuming to train.
- With no cuda acceleration, the prediction process for a pair of images would take about 10 to 20 seconds which is far from running in real time at the miliseconds level.
- As mentioned above, most codebase are specialized for benchmark and it is hard to run custom pairs of images. For mobilestereonet, it requires input image to be less than 1248x384.
- It is also hard to find out what is the actual disparity value in pixels, since output is often colorized with no standards. One reason we choose this codebase is that it's relavely easy to extract out the real disparity map.
- In the end, we decided to run an experiment on how well the models produced by training on different datasets peforms on five pairs of various types of images, based on what we've learned in class and our knowledge of the dateset used for training.

#### The experiment
The input images are in the img folder.
- Chess, and Hall are indoor scene from Middlebury dataset
- Kitchen is photo taken by ourselves
- Kitti is from the Kitti dataset
- Scene is a 3d model rendered scene from University of Tsukuba

**Input left image preview**
| Chess                       | Hall                      | Kitchen                         | Kitti                       | Scene                       |
|-----------------------------|---------------------------|---------------------------------|-----------------------------|-----------------------------|
| ![chess_l](img/chess_l.png) | ![hall_l](img/hall_l.png) | ![kitchen_l](img/kitchen_l.png) | ![kitti_l](img/kitti_l.png) | ![scene_l](img/scene_l.png) |

Output disparity maps (note that they do not scale by the same scalar from the real disparity in pixels)
**Chess**
| SF                                               | SF+DS                                              | SF+DS+KITTI2015                                         |
|--------------------------------------------------|----------------------------------------------------|---------------------------------------------------------|
| ![chess_sf](neural_network/output_chess_l_1.png) | ![chess_sfds](neural_network/output_chess_l_2.png) | ![chess_sfdskitti](neural_network/output_chess_l_3.png) |

**Hall**
| SF                                               | SF+DS                                              | SF+DS+KITTI2015                                         |
|--------------------------------------------------|----------------------------------------------------|---------------------------------------------------------|
| ![hall_sf](neural_network/output_hall_l_1.png) | ![hall_sfds](neural_network/output_hall_l_2.png) | ![hall_sfdskitti](neural_network/output_hall_l_3.png) |

**Kitchen**
| SF                                               | SF+DS                                              | SF+DS+KITTI2015                                         |
|--------------------------------------------------|----------------------------------------------------|---------------------------------------------------------|
| ![kitchen_sf](neural_network/output_kitchen_l_1.png) | ![kitchen_sfds](neural_network/output_kitchen_l_2.png) | ![kitchen_sfdskitti](neural_network/output_kitchen_l_3.png) |

**Kitti**
| SF                                               | SF+DS                                              | SF+DS+KITTI2015                                         |
|--------------------------------------------------|----------------------------------------------------|---------------------------------------------------------|
| ![kitti_sf](neural_network/output_kitti_l_1.png) | ![kitti_sfds](neural_network/output_kitti_l_2.png) | ![kitti_sfdskitti](neural_network/output_kitti_l_3.png) |

**Scene**
| SF                                               | SF+DS                                              | SF+DS+KITTI2015                                         |
|--------------------------------------------------|----------------------------------------------------|---------------------------------------------------------|
| ![scene_sf](neural_network/output_scene_l_1.png) | ![scene_sfds](neural_network/output_scene_l_2.png) | ![scene_sfdskitti](neural_network/output_scene_l_3.png) |

**Observations & Possible Explanations**
- For chess and hall images, SF model performs much better compared to SF+DS and SF+DS+KITTI2015 in terms of revealing more close up depth details like the chess pieces, the chair, and folded up chair in the hall. We guess that this happens because DS and KITII2015 are both stereo datasets for driving with pictures on the streets where items are far away and have less disparity in pixels movement compared to more closed up objets, which makes the later two models only sensitive to blocks of far away objects.
- For the kitchen image taken by ourselves, three models all failed to produce a clear disparity output. Our guess is that the white light bar type of object is not present in all three datasets, making the models having a hard time to predict the disparity of the closets near the light bar.
- For the kitti image, SF+DS+KITTI2015 performs the best in reavealing the most details like the trees. It's expected since this image is from the kitti testing, and is similar to the training data in kitti.
- For the scene image, SF model performs the best, we can see the statue, the lamp, the camera, the cans and even some not so clear bookshelf. It's also reasonable because Scene Flow Dataset has FlyingThings3D that are similar 3D rendered scenes.

### Components from preexisting work (code from github, other libraries)

- For the neural network part, we used code from [MobileStereoNet](https://github.com/cogsys-tuebingen/mobilestereonet))

### Components implemented for the project (new code)

- For the neural network part, we wrote a new script to visualize disparity maps ([visualize_disparity.py](neural_network/visualize_disparity.py))


## What we've learned & other thoughts
- Neural Networks could achieve a lot in the field of Computer Vision, but for the specific task of stereo depth estimation, images that are not driving street photos may not get an accurate output due to the limitation of the dataset not having much indoors training images. If we want to achieve better results for indoor images, we may need to finetune on an indoor focused stereo dataset after pretraining on Scene Flow.

## Citation & Credits

