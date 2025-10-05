<!-- image -->

<!-- image -->

Antoun Khawaja

## Automatic ECG Analysis using Principal Component Analysis and Wavelet Transformation

## Vol. 3

## Karlsruhe Transactions on Biomedical Engineering

Editor: Universität Karlsruhe (TH) Institute of Biomedical Engineering

## Automatic ECG Analysis using Principal Component Analysis and Wavelet Transformation

von Antoun Khawaja

<!-- image -->

Dissertation, Universität Karlsruhe (TH) Fakultät für Elektrotechnik und Informationstechnik, 2006

## Impressum

Universitätsverlag Karlsruhe c/o Universitätsbibliothek Straße am Forum 2 D-76131 Karlsruhe www.uvka.de

<!-- image -->

Dieses Werk ist unter folgender Creative Commons-Lizenz lizenziert: http://creativecommons.org/licenses/by-nc-nd/2.0/de/

Universitätsverlag Karlsruhe 2007 Print on Demand

ISSN: 1864-5933

ISBN:  978-3-86644-132-3

## Automatic ECG Analysis Using Principal Component Analysis And Wavelet Transformation

Zur Erlangung des akademischen Grades eines

## DOKTOR-INGENIEURS

von der FakultΥ at fΥ ur Elektrotechnik und Informationstechnik der UniversitΥ at Fridericiana Karlsruhe genehmigte

## DISSERTATION

von

Dipl.-Ing. Antoun Khawaja aus Damaskus Syrien

Tag der mΥ undlichen PrΥ ufung:

23. November 2006

Hauptreferent:

Prof. Dr. rer. nat. Olaf DΥ ossel

1. Korreferent:

Dr. Ghazwan Butrous

2. Korreferent:

Prof. Dr.-Ing. Uwe Kiencke

## 1

## Aknowledgements

I would like to address my special thanks to my advisor, Prof. Dr. rer. nat. Olaf D¨ ossel , for his endless and valuable supports, for his great advices and for providing me a nice opportunity to carry out my research in a pleasant working environment at IBT, Institut f¨ ur Biomedizinische Technik, Universit¨ at Karlsruhe (TH). I extend my profound sense of gratitude to Dr. Ghazwan Butrous for his important moral support, for making very important materials and ECG signals available for me and for a very nice and fruitful collaboration between IBT and him, as the chief scientific officer for Pfizer Ltd, UK. I also would like to thank Prof. Dr.-Ing. Uwe Kiencke deeply for his insightful comments and valuable suggestions. Very kind thanks to Dr. Valentin Demmel and his wife Dr. Gerda Demmel for helping me evaluating some of the methods presented in this research thesis and for a nice cooperation with their company, nabios GMBH. Their collaboration and help are really highly acknowledged and appreciated. I am thankful to all my friends, colleagues, administrative staff and the technical staff in the institute for creating an optimal working atmosphere and for their cooperation in the completion of my thesis. Special thanks to my friend and colleague MEng (Trip. Dipl.) Matthias Reumann and again to Prof. Dr. rer. nat. Olaf D¨ ossel for the correction of this written thesis. I am deeply grateful to my great mother and brother, Georgette and Nicolas Khawaja. They did always their best to help me and offered me very helpful spiritual support. My great thanks also to Ms. Ho Thi Dieu Van, who always encouraged me in the best possible way and kept permanently supporting me. I would like to thank very deeply Prof. Hans Bienlein and his wife Melanie Bienlein for their valuable support and their helpful warmhearted advices. They always made me feel at home. My sincere gratitude is expressed to Mrs. Sebanti Sanyal, Mr. Sebastian Seitz, Ms. Liza Mahey and Ms. Julia Bohnert, whose projects were supervised by me, for their perfect team-working atmosphere and their nice scientific contributions. Finally, I would like to thank the Catholic Academic Exchange Service (KAAD), www.kaad.de, for providing funds to support this research.

## Introduction

Bioelectrical signals express the electrical functionality of different organs in the human body. The Electrocardiogram, also called ECG signal, is one important signal among all bioelectrical signals. The ECG reflects the performance and the properties of the human heart and conveys very important hidden information in its structure. This information has to be extracted and analysed before any useful and meaningful interpretations can be started. Extracting or decoding this information or feature from ECG signal has been found very helpful in explaining and identifying various pathological conditions. The feature extraction procedure can be accomplished straightforward by analysing the ECG visually on paper or screen. However, the complexity and the duration of ECG signals are often quite considerable making the manual analysis a very time-consuming and limited solution. In addition, manual feature extraction is always prone to error. Therefore, ECG signal processing has become an indispensable and effective tool for extracting clinically significant information from ECG signals, for reducing the subjectivity of manual ECG analysis and for developing advanced aid to the physician in making well-founded decisions. Over the past few years automatic analysis of electrocardiograms (ECGs) has gained more and more significance in the field of clinical ECG diagnosis.

ECG analysis systems are usually designed to process ECG signals measured under particular conditions, like resting ECG interpretation, stress test analysis, ambulatory ECG monitoring, intensive care monitoring, etc...

However, preconditioning the recorded ECG signals is a common point to all these systems. In the preconditioning stage, ECG signals need to be filtered from different types of noise, segmented, delineated with respect to their waves and complexes and prepared for the further analysis.

The complexity of an ECG analysis algorithm depends much on the application. For instance, the noise reduction algorithm in ambulatory monitoring is much more complicated than the one in resting ECG analysis.

Furthermore, ECG analysis algorithms are designed for at least one of three major clinical contexts, which are diagnosis, therapy and monitoring.

ECG signal processing algorithms form an important part of systems for monitoring of patients who suffer from a life-threatening condition. Monitoring algorithms should be able to detect the predisposition to a dangerous cardiac disorder before occuring and provide an alarm to save the life of the patient. The life-threatening condition can be pronounced by a drug-induced ventricular tachyarrhythmia. This kind of tachyarrhyth-

mia is called Torsade de Pointes (TDP). TDP is a dangerous life-threatening arrhythmia, because it can degenerate into ventricular fibrillation, leading to sudden death.

Drug evaluation with respect to effects on the heart action has become a major focus for the determination of drug safety and cardiac safety. An undesirable property of some nonantiarrhythmic drugs is their ability to delay cardiac repolarization. This delay creates an electrophysiological environment that favors the development of cardiac arrhythmias, most clearly Torsade de Pointes (TDP), but possibly other ventricular tachyarrhythmia as well. Two main features of TDP, as observed from real ECG signals of patients before its episode, are pronounced first with marked prolongation of the duration between ventricular depolarization and repolarization, known as QT interval, and second with large morphology changes of the T wave, respresenting the variance of ventricular repolarization in ECG signal from one cardiac cycle, also called beat, to another. In particular, QT interval has been identified as a surrogate marker for possible proarrhythmic effects, i.e. for clinical assessment of drug safety. In fact, QT interval is the simplest clinical measure that is available at present. On the other hand, analysing T wave morphology (TWM) changes in beat-to-beat manner seems to be more complicated than measuring simply QT interval and appears to play a more important role in accessing the electrical stability of the ventricles and furthermore in detecting predisposition to TDP. That is, analysing the beat-to-beat variability in TWM seems to be a robust precursor to TDP as noticed in ECG signal.

## 2.1 Aim and Objectives of this Thesis

The main objective of this thesis is developing methods to analyse and detect small changes in ECG waves and complexes that indicate cardiac diseases and disorders. Detecting predisposition to Torsade de Points (TDP) by analysing the beat-to-beat variability in T wave morphology before and after TDP episode is the main core of this thesis. Detecting small changes in QRS complex and predicting future QRS complexes of patients from a time series of ECG signals is the second main topic of this research thesis. The third main point is to cluster similar ECG components, namely T waves, depending on their morphologies in different groups and to find the main dominant T wave morphology or morphologies for every ECG signal. In order to establish and achieve the mentioned aims, the following objectives have to be fulfilled:

1. ECG Signal Preconditioning : Novel techniques for low-frequency and high-frequency noise cancellation as well as ECG fiducial points detection have been developed using the power of the time-frequency analysis, namely Wavelet transformation. Some other new preconditioning algorithms for detecting outliers in ECG signal and for ECG wave and complex alignment were also carried out.
2. Morphological Feature Extraction : Morphological features have been extracted from ECG signals after applying the preconditioning stage. The extraction is based on using Principal Component Analysis (PCA), also called Karhunen-Lo` eve transform (KLT). This technique is a multivariate statistical technique that allows for the identification of key variables, or combinations of variables, in a multidimensional data set that

best explains the small differences between individual observations. In this study, the observations are ECG waves or complexes from all cardiac beats of an ECG signal.

3. Analysis of the Morphological Features : After extracting the morphological features from similar ECG components, further analysis will be applied depending on the application.

As mentioned already, this research thesis is based on using PCA as a linear transformation technique in extracting morphological features from ECG signals. More and further investigations will be done in the future by using nonlinear techniques in addition to PCA in order to examine any inherently nonlinear underlying structure in ECG signal.

## 2.2 Organization of the Thesis

The thesis is divided into four parts. The first part, including chapter 3 and chapter 4, provides the medical and technical basics and foundations necessary for the understanding of ECG signal, the electrophysiological processes in the heart and the terminology used throughout the thesis. Chapter 3 describes the anatomy and the physiology of the human heart, ECG lead systems and normal ECG signal, normal heart rhythms and different arrhythmias as well as heartbeat morphologies. Chapter 4 addresses the technical aspects of ECG recording including ECG electrodes, ECG artifacts and interference and ECG amplifiers. Chapter 4 includes also the databases used in this thesis.

The second part includes chapter 5 and chapter 6. Chapter 5 describes the mathematical background of all the methods used in this thesis including Wavelet transformation, PCA etc... Whereas, chapter 6 provides the state of the art in ECG signal processing.

The third part of this thesis, chapter 7, includes all the ECG signal preconditioning developed and used in this thesis.

The fourth and the last part, chapter 8 and chapter 9, addresses the methods for detecting predisposition to Torsade de Points (TDP), T wave clustering, QRS complex temporal and spatiotemporal analysis as well as the analysis for predicting future QRS complexes along with their results.

## Contents

| 1   | Aknowledgements . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                | 3   |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
| 2   | Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                       | 5   |
|     | 2.1 Aim and Objectives of this Thesis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                        | 6   |
| 2.2 | Organization of the Thesis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                       | 7   |
| 3   | Medical Foundations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                  | 1   |
| 3.1 | Heart Anatomy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                | 1   |
|     | 3.1.1 Heart Structure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                    | 2   |
|     | 3.1.2 Myofiber Orientation of Cardiac Muscle. . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                      | 7   |
| 3.2 | . . . . . . . . . . . . . . .                                                                                                                                                                                                                  | 8   |
|     | Electrophysiology of the Heart . . . . . . . . . . . . . . . . . . . . . 3.2.1 Resting Voltage, Action Potential and Refractory Periods of a Single Cell of Working Myocardium . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . | 8   |
|     | 3.2.2 Excitation Propagation and Cardiac Contractions . .                                                                                                                                                                                      | 11  |
|     | . . . . . . . . . . . . 3.2.3 The Generation of an Electrocardiogram and the Dominant Cardiac . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                      | 13  |
| 3.3 | Vector. . . . . . . . . . . . . . . . . . . . . . ECG Lead Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                   | 14  |
|     | 3.3.1 The Conventional 12-lead System . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                  | 14  |
|     | 3.3.2 The Corrected Orthogonal Leads . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                   | 19  |
|     | 3.3.3 Body-Surface Mapping Lead Systems . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                      | 20  |
|     | 3.3.4 Ambulatory Monitoring Leads . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                | 21  |
| 3.4 | The Normal ECG Waves, Time Intervals, and its Normal Variants . . . . .                                                                                                                                                                        | 23  |
|     | 3.4.1 The P Wave . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                   | 23  |
|     | . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                                      | 25  |
|     | 3.4.3 The PR or PQ Interval                                                                                                                                                                                                                    |     |
|     | 3.4.4 The T Wave . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                 | 25  |
|     | 3.4.5 The U Wave . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                     | 25  |
|     | 3.4.6 The PP Interval and the RR Interval . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                    | 25  |
|     | The QT Interval . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                              | 26  |
|     | 3.4.7 . .                                                                                                                                                                                                                                      |     |
|     | 3.4.8 The ST Segment. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                      | 26  |
| 3.5 | Heart Rhythms and Arrhythmias . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                | 27  |
|     | 3.5.1 Sinus Rhythm . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                   | 27  |

|     | 3.5.3 Atrial Arrhythmia . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                               |   28 |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|
|     | 3.5.4 Ventricular Arrhythmia . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                  |   29 |
|     | 3.5.5 Wolff-Parkinson-White Syndrome . . . . . . . . . . . . . . . . . . . .                                                                                                            |   30 |
|     | 3.5.6 Heart Conduction Blocks . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                     |   31 |
| 3.6 | Heartbeat Morphologies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                |   31 |
|     | 3.6.1 Ischemic Heart Disease . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                  |   31 |
|     | 3.6.2 Myocardial Infarction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                 |   32 |
|     | 3.6.3 Long QT Syndromes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                   |   32 |
|     | 3.6.4 Brugada Syndrome. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                 |   33 |
|     | 3.6.5 T-Wave Alternans . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                |   33 |
| 3.7 | Torsade de Pointes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                          |   35 |
|     | Technical Aspects of ECG Recording and Databases Used                                                                                                                                   |   39 |
| 4.1 | The Electrode Skin Interface . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                  |   39 |
|     | 4.1.1 Electrochemical Potentials . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                    |   39 |
|     | 4.1.2 Reversible and Nonreversible Electrodes . . . . . . . . . . . . . .                                                                                                               |   40 |
|     | 4.1.3 Electrodes of the First and Second Kind . . . . . . . . . . . . . .                                                                                                               |   40 |
|     | 4.1.4 Polarization or Overvoltages. . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                     |   40 |
|     | 4.1.5 Electrical Properties of the Skin . . . . . . . . . . . . . . . . . . . . .                                                                                                       |   40 |
|     | 4.1.6 Electrode Skin Impedance and Offset Voltage . . . . . . . . . .                                                                                                                   |   42 |
| 4.2 | Types of Electrodes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                           |   43 |
|     | 4.2.1 Plate Electrodes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                            |   44 |
|     | 4.2.2 Suction Electrodes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                              |   44 |
|     | 4.2.3 Fluid-Column Electrodes . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                     |   45 |
|     | 4.2.4 Active Electrodes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                             |   46 |
| 4.3 | Electrode Pastes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                        |   46 |
| 4.4 | ECG Artifacts and Interference . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                    |   47 |
|     | 4.4.1 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                        |   47 |
|     | 4.4.2 Artifact Potentials . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                             |   49 |
|     | 4.4.3 Electromagnetic Field Interference . . . . . . . . . . . . . . . . . . .                                                                                                          |   50 |
| 4.5 | ECG Amplifiers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                          |   52 |
|     | 4.5.1 Differential and Instrumentation Amplifiers . . . . . . . . . . .                                                                                                                 |   53 |
|     | 4.5.2 Amplifier Specification . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                 |   54 |
| 4.6 | IBT Multi-Channel ECG Acquisition System . . . . . . . . . . . . . . .                                                                                                                  |   56 |
|     | 4.6.1 The First System ' SynAmps ' . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                      |   57 |
|     | 4.6.2 The Second System ' ActiveTwo ' . . . . . . . . . . . . . . . . . . . . .                                                                                                         |   58 |
| 4.7 | IBT Multi-Channel ECG Lead System . . . . . . . . . . . . . . . . . . . . .                                                                                                             |   61 |
| 4.8 | ECG Databases. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                          |   62 |
|     | 4.8.1 Multi-Channel ECG Databases . . . . . . . . . . . . . . . . . . . . . .                                                                                                           |   62 |
|     | 4.8.2 Annotated ECG Databases . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                         |   63 |
|     | 4.8.3 Clinical-Trials ECG Databases. . . . . . . . . . . . . . . . . . . . . . .                                                                                                        |   65 |
|     | . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                           |   69 |
|     | Applied Methods and Mathematics                                                                                                                                                         |   69 |
| 5.1 | Mathematical Basics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5.1.1 Expected Value. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . |   69 |

|         | 5.1.2 Variance and Covariance . . . . . . . . . . . . . . . . . . . .                  | . . 69   |
|---------|----------------------------------------------------------------------------------------|----------|
|         | 5.1.3 Correlation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        | . . 70   |
| 5.2     | Principal Component Analysis (PCA) . . . . . . . . . . . . .                           | . . 71   |
|         | 5.2.1 Orthogonal and Orthonormal Series Expansions.                                    | . . 72   |
|         | 5.2.2 Truncated Orthonormal Series Expansions . . . .                                  | . . 72   |
|         | 5.2.3 Karhunen-Lo` eve Expansion . . . . . . . . . . . . . . . . .                     | . . 73   |
|         | 5.2.4 Methods to Calculate PCA . . . . . . . . . . . . . . . . .                       | . . 75   |
|         | 5.2.5 Hotelling's T Squared Statistics . . . . . . . . . . . . . .                     | . . 79   |
| 5.3     | Finite & Infinite Impulse Response Filters . . . . . . . . . .                         | . . 80   |
|         | 5.3.1 Z-Transform . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          | . . 80   |
|         | 5.3.2 Laplace Transform . . . . . . . . . . . . . . . . . . . . . . . .                | . . 81   |
|         | 5.3.3 LTI System Theory . . . . . . . . . . . . . . . . . . . . . . . .                | . . 82   |
|         | 5.3.4 Finite Impulse Response Filter (FIR) . . . . . . . . .                           | . . 82   |
|         | 5.3.5 Infinite Impulse Response Filter (IIR) . . . . . . . .                           | . . 83   |
|         | 5.3.6 Butterworth Filter . . . . . . . . . . . . . . . . . . . . . . . . .             | . . 85   |
| 5.4     | Wavelets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . | . . 87   |
|         | 5.4.1 Development of Wavelet Theory . . . . . . . . . . . . .                          | . . 87   |
|         | 5.4.2 Multiresolution Signal Analysis . . . . . . . . . . . . . .                      | . . 90   |
|         | 5.4.3 Continuous Wavelet Transform (CWT) . . . . . . .                                 | . . 91   |
|         | 5.4.4 The Dyadic Wavelet Transform (DyWT). . . . . .                                   | . . 92   |
|         | 5.4.5 Discrete Wavelet Transform (DWT) . . . . . . . . . .                             | . . 93   |
|         | 5.4.6 Implementation of the DWT Using Filter Banks                                     | . . 97   |
|         | 5.4.7 Properties of DWT Orthogonal Wavelet . . . . . .                                 | . . 103  |
|         | 5.4.8 Discrete Stationary Wavelet Transform (SWT)                                      | . . 106  |
|         | 5.4.9 Discrete Wavelet Packets Transform (DWPT) .                                      | . . 106  |
| 6 State | of the Art In ECG Signal Processing . . . . . .                                        | . . 109  |
| 6.1     | Baseline Wander . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        | . . 109  |
| 6.2     | ECG Segmentation and Fiducial Points Detection . . .                                   | . . 110  |
|         | 6.2.1 QRS Complex Detection Algorithms . . . . . . . . .                               | . . 110  |
| 6.3     | 6.2.2 Delineation Algorithms . . . . . . . . . . . . . . . . . . . . .                 | . . 112  |
|         | PCA Applications on ECG Signal . . . . . . . . . . . . . . . . .                       | . . 115  |
| 7 ECG   | Signal Preconditioning . . . . . . . . . . . . . . . . . . . . .                       | . . 117  |
| 7.1     | ECG Signal Low-Frequency Filtering . . . . . . . . . . . . . .                         | . . 117  |
|         | 7.1.1 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       | . . 117  |
|         | 7.1.2 Simulation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       | . . 117  |
|         | 7.1.3 Simulation Result . . . . . . . . . . . . . . . . . . . . . . . . . .            | . . 120  |
|         | 7.1.4 Discussion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       | . . 120  |
|         | 7.1.5 Proposed Method . . . . . . . . . . . . . . . . . . . . . . . . . .              | . . 121  |
|         | 7.1.6 Results of Application on Real ECG. . . . . . . . . .                            | . . 121  |
| 7.2     | ECG Signal Denoising . . . . . . . . . . . . . . . . . . . . . . . . . . .             | . . 122  |
|         | 7.2.1 Single-Channel ECG Denoising . . . . . . . . . . . . . .                         | . . 122  |
| 7.3     | ECG Noise Estimation . . . . . . . . . . . . . . . . . . . . . . . . . . . .           | . . 128  |
|         | 7.3.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . .             | . . 128  |

|     | 7.3.2 ECG Low-Frequency Estimation . . . . . . . . . . . . . . . .                         | 129   |
|-----|--------------------------------------------------------------------------------------------|-------|
|     | 7.3.3 ECG High-Frequency Estimation . . . . . . . . . . . . . . .                          | 130   |
|     | 7.3.4 Applications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       | 130   |
| 7.4 | ECG Delineation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        | 133   |
|     | 7.4.1 Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     | 133   |
|     | 7.4.2 Single Channel Delineation Strategy . . . . . . . . . . . . .                        | 139   |
|     | 7.4.3 Multi-Channel ECG Delineation . . . . . . . . . . . . . . . .                        | 146   |
|     | 7.4.4 Multi-Channel ECG Delineation Results . . . . . . . . .                              | 147   |
|     | 7.4.5 Single ECG Delineation Validation . . . . . . . . . . . . . .                        | 147   |
|     | 7.4.6 Discussion and Conclusion . . . . . . . . . . . . . . . . . . . . .                  | 149   |
| 7.5 | ECG-Complex and ECG-Wave Extraction. . . . . . . . . . . . .                               | 150   |
| 7.6 | Detecting Outliers in the Automatic ECG Segmentation                                       | 150   |
|     | 7.6.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       | 150   |
|     | 7.6.2 Method . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     | 152   |
|     | 7.6.3 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  | 153   |
|     | 7.6.4 Discussion and Conclusion . . . . . . . . . . . . . . . . . . . . .                  | 154   |
| 7.7 | ECG-Complex and ECG-Wave Fine Alignment . . . . . . . .                                    | 154   |
|     | T-Wave Morphology Analysis . . . . . . . . . . . . . . . . . . . . . . . .                 | 159   |
| 8.1 | Detecting Predisposition to 'Torsad de Points' . . . . . . . . .                           | 159   |
|     | 8.1.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       | 159   |
|     | 8.1.2 Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    | 160   |
|     | 8.1.3 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  | 168   |
|     | 8.1.4 Discussion and Conclusions . . . . . . . . . . . . . . . . . . . .                   | 169   |
| 8.2 | T-Wave Morphology Clustering . . . . . . . . . . . . . . . . . . . . . .                   | 169   |
|     | 8.2.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       | 169   |
|     | 8.2.2 Method . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     | 170   |
|     | 8.2.3 Result . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . | 172   |
|     | 8.2.4 Discussion and Conclusion . . . . . . . . . . . . . . . . . . . . .                  | 172   |
|     | QRS Complex Morphology Analysis . . . . . . . . . . . . . . . . .                          | 185   |
|     | . .                                                                                        |       |
|     | 9.1.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           | 185   |
|     | 9.1.2 Databases Used . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           | 185   |
|     | 9.1.3 Defining Respiration & Heart Rate Vectors . . . . . . .                              | 185   |
|     | 9.1.4 Data Preconditioning. . . . . . . . . . . . . . . . . . . . . . . . . .              | 186   |
|     | 9.1.5 Temporal Analysis of QRS Complex. . . . . . .                                        | 186   |
|     | . . . . . . 9.1.6 Spatio-Temporal Analysis of QRS Complex . . . . . .                      | 192   |
|     | 9.1.7 Discussion and Conclusion . . . . . . . . . . . . . . . . . . . . .                  | 195   |
| 9.2 | Predicting QRS Complex . . . . . . . . . . . . . . . . . . . . . . . . . . .               | 195   |
|     | 9.2.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       | 195   |
|     | 9.2.2 Single-Channel ECG Signal Preconditioning . . . . . .                                | 195   |
|     | 9.2.3 Method . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     | 196   |
|     | 9.2.4 Validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     | 197   |
|     | 9.2.5 Discussion and Conclusion . . . . . . . . . . . . . . . . . . . . .                  | 198   |

| Contents     | IX    |
|--------------|-------|
| A Appendix A | . 201 |

Bibliography

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

205

## List of Figures

|   3.1 | The location and the orientation of the human heart in the chest. . . . . . .                                                                                                                                                                                  |   2 |
|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
|  3.2  | Heart chambers, systemic and pulmonary circulations . . . . . . . . . . . . . . . .                                                                                                                                                                            |   3 |
|  3.3  | Cut-away diagram of cardiac muscle showing several microfibrils and associated sarcoplasmic reticulum and the sarcolemma and t-tubular systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . |   3 |
|  3.4  | The typical structure of the sarcolemma and the voltage-gated ion channel.                                                                                                                                                                                     |   4 |
|  3.5  | Structure of a typical voltage-gated ion channel . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                                     |   5 |
|  3.6  | The structure of a sacromere . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                         |   6 |
|  3.7  | The structure of the thick and thin filaments . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                                    |   7 |
|  3.8  | The conduction system of the heart . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                               |   8 |
|  3.9  | The cardiac fiber orientation for the heart demonstrated on the heart of the Visible Man . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                       |   9 |
|  3.1  | The Action Potential of a single cell of working Myocardium. . . . . . . . . . .                                                                                                                                                                               |  10 |
|  3.11 | The resting voltage and action potential electrophysiology of a single cell of working myocardium. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                         |  11 |
|  3.12 | Schematic diagram of the major cellular components involved in contraction of the myocyte. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                       |  12 |
|  3.13 | The Genesis of Electrocardiogram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                             |  13 |
|  3.14 | Einthoven limb leads and Einthoven triangle . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                                    |  15 |
|  3.15 | The generation of the ECG signal in the Einthoven limb leads. . . . . . . . .                                                                                                                                                                                  |  16 |
|  3.16 | The Augmented Unipolar Limb Leads, aV R,aV L, and aV F . . . . . . . . . .                                                                                                                                                                                     |  17 |
|  3.17 | The Unipolar Precordial Leads.. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                          |  17 |
|  3.18 | The direction of the bipolar limb leads and the augmented limb leads in the frontal plane and the precordial leads in the transversal plane. . . . . .                                                                                                         |  18 |
|  3.19 | The modified electrode positions for the limbs according to Mason and Likar . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                |  19 |
|  3.2  | Electrodes of the Amsterdam 62-lead body surface mapping set . . . . . . . .                                                                                                                                                                                   |  21 |
|  3.21 | The recommended electrode positions for two-channel ambulatory ECG recording according to the Committee on Electrocardiography of in the American Heart Association . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                |  22 |
|  3.22 | Schematic diagram of normal sinus rhythm for a human heart as seen on ECG. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                 |  23 |
|  3.23 | The power spectrum of the P wave, QRS Complex and T wave.. . . . . . . .                                                                                                                                                                                       |  24 |

| 3.24      | Different morphologies of QRS complex. . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                  | 25   |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|
| 3.25      | The premature ventricular contraction (PVC).. . . . . . . . . . . . . . . . . . . . . . .                                                                                                       | 27   |
| 3.26      | An example of Bigeminy. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                       | 28   |
| 3.27      | An example of Couplet. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                      | 28   |
| 3.28      | Atrial flutter and atrial fibrillation. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                         | 29   |
| 3.29      | An example of ventricular flutter. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                          | 30   |
| 3.30      | An example of ventricular flutter. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                          | 31   |
| 3.31      | An example of T-wave alternans. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                             | 34   |
| 3.32      | The typical initiation of TDP in ECG signal after short-long-short cycle sequences. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . | 36   |
| 3.33      | different morphologies of QRS complex . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                 | 38   |
| 4.1       | Factors that influence the skin impedance . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                 | 41   |
| 4.2       | A complete electrode-skin interface considering most of the relevant effects                                                                                                                    | 42   |
| 4.3       | Two examples of plate electrodes used in routine electrocardiography . . .                                                                                                                      | 44   |
| 4.4       | Two examples of suction electrodes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                              | 45   |
| 4.5       | The principle of fluid-column electrodes . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                | 46   |
| 4.6       | The typical configuration for an ECG acquisition system . . . . . . . . . . . . . .                                                                                                             | 47   |
| 4.7       | The equivalent electric circuit of the typical configuration for ECG acquisition system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           | 48   |
| 4.8       | The basic layout of ECG amplifiers. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                             | 52   |
| 4.9       | Differential amplifier schematic. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                         | 53   |
| 4.10      | Differential amplifier schematic. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                         | 54   |
| 4.11      | Increasing the common-mode voltage rejection (CMR) by the driven-ground technique . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                             | 56   |
| 4.12      | The shielded cables assembled to be used with SynAmps system . . . . . .                                                                                                                        | 57   |
| 4.13      | Two SynAmps main units and two headboxes placed on one of the main unit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   | 58   |
| 4.14      | ST segment distortion due to the 50/60 Hz digital notch filter in the SynAmps system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .              | 59   |
| 4.15      | The Flat-Type active electrodes for the multi-channel ECG ActiveTwo System . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    | 60   |
| 4.16      | The Active BSPM Carbon Strips for multi-channel ECG ActiveTwo System . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .            | 60   |
| 4.17      | Multi-channel ECG ActiveTwo AD-box with battery .                                                                                                                                               | 61   |
| 4.18      | . . . . . . . . . . . . . . . . The 32-lead Lux limited recording array estimating the complete 192-lead data on 132 subjects by Lux et al with 6 electrodes on the back . . . . . . .          |      |
| 4.19      | The 32-lead Lux anterior recording array estimating the complete 192-lead data on 132 subjects by Lux et al without any electrodes on the                                                       | 63   |
|           | back . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                      | 64   |
| 4.20 4.21 | The IBT 64-Channel ECG Lead System based on Lux limited . . . . . . . . . The IBT 64-Channel ECG Lead positions on the human torso with the                                                     | 65   |
| 4.22      | corresponding electrode labels . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . The IBT Multi-Channel ECG electrode set applied on a young volunteer                   | 66   |

|   4.23 | A screen-shot during one of the IBT 64-Channel ECG recordings with the SynAmps system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                               |   67 |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|
|   4.24 | The IBT Multi-Channel ECG electrode set and the respiration belt attached to a young volunteer during one measurement with the ActiveTwo system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . |   67 |
|   4.25 | A screen-shot during one of the IBT 64-Channel ECG recordings with the ActiveTwo system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                               |   68 |
|   5.1  | The gain of Butterworth low-pass filters of orders 1 through 5 . . . . . . . . .                                                                                                                                                              |   86 |
|   5.2  | A comparison between Butterworth filter and other linear filters . . . . . . .                                                                                                                                                                |   88 |
|   5.3  | Time-Frequency Resolution at different signal representations . . . . .                                                                                                                                                                       |   91 |
|   5.4  | . . . . The calculation of the DWT coefficients implemented using the two-channel analysis filter bank. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                       |   99 |
|   5.5  | . . . The calculation of the DWT through successive decomposition of the approximation coefficients . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                           |  100 |
|   5.6  | The dyadic tree structure implementing the inverse DWT . . . . . . . . . . . . .                                                                                                                                                              |  102 |
|   5.7  | The Haar Wavelet Function . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                       |  106 |
|   7.1  | The 8 th , 9 th and 10 th level approximation coefficients for an ECG signal with a sample frequency equal to 1 kHz . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                   |  118 |
|   7.2  | An example of the noise-free ECG generated by Savitzky-Golay filter simulator in Matlab Environment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                       |  119 |
|   7.3  | The structure of each matrix derived from the baseline simulation process                                                                                                                                                                     |  120 |
|   7.4  | The influence of using the conventional high-pass filter to remove the baseline wander on the ECG morphology and ST segment . . . . . . . . . . .                                                                                             |  122 |
|   7.5  | . The influence of using our wavelet-based technique to remove the baseline wander on the ECG morphology and ST segment . . . . . . . . . . . . . . . . . . . .                                                                               |  123 |
|   7.6  | Baseline cancellation result on record number 113, channel1, from MIT- Arrhythmia Database using our wavelet-based baseline filter . . . . . . . . . . .                                                                                      |  123 |
|   7.7  | Baseline cancellation result on an arbitrary ECG segment from a recorded multi-channel signal using our wavelet-based baseline filter . . . . . . . . . . . .                                                                                 |  124 |
|   7.8  | The percentage mean similarity results for all mother wavelets employed in the denoising simulation. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                            |  127 |
|   7.9  | The result of applying our wavelet-method with Symlet2 on a real ECG signal taken from one research study of Pfizer LTD . . . . . . . . . . . . . . . . . . .                                                                                 |  127 |
|   7.1  | The improvement of the common-mode rejection ratio (CMRR) for the new ECG signal referring to WCT . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                             |  129 |
|   7.11 | Baseline wander cancellation in a real 30-minute ECG segments from the first channel of a 2-channel long-time ECG tape. . . . . . . . . . . . . . . . . . . . . .                                                                             |  131 |
|   7.12 | The baseline wander estimation signal ELFE of the ECG signal shown in figure 7.11. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                        |  132 |
|   7.13 | The high-frequency noise elimination in the ECG signal filtered from the effect of baseline wander illustrated in figure 7.11. . . . . . . . . . . . . . . . . . . .                                                                          |  133 |
|   7.14 | High-frequency noise elimination result in the three subsegments, 'A', 'B' and 'C', shown in figure 7.13. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                           |  134 |

|   7.15 | The high-frequency noise estimation of a 2-hour ECG signal whose first quarter is shown in figure 7.13. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                          |   135 |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|   7.16 | The result of a retrospective baseline wander analysis on 1246 ECG signals from a Phase I study. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                           |   135 |
|   7.17 | The First Level Details Signal (FLDS) obtained from a straight line signal with constant slope . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                             |   136 |
|   7.18 | The First Level Details Signal (FLDS) obtained from a symmetric positive triangular pulse . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                          |   137 |
|   7.19 | The First Level Details Signal (FLDS) obtained from a symmetric negative triangular pulse . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                            |   137 |
|   7.2  | Deriving FLDS, DCM and DCS from a cosine signal. . . . . . . . . . . . . . . . . . .                                                                                                                                                                     |   138 |
|   7.21 | Deriving FLDS, DCM and DCS from a real QRS complex. . . . . . . . . . . . . .                                                                                                                                                                            |   139 |
|   7.22 | Deriving FLDS, DCM and DCS from a real P wave. . . . . . . . . . . . . . . . . . . .                                                                                                                                                                     |   140 |
|   7.23 | Deriving FLDS, DCM and DCS from a real T wave.. . .                                                                                                                                                                                                      |   140 |
|   7.24 | . . . . . . . . . . . . . . . . Detecting the fiducial points of a real ECG cycle using DCM and DCS values. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                          |   141 |
|   7.25 | Detecting R peak. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                        |   143 |
|   7.26 | Enhancement of R Peak and QRS complex detection. . . . . . . . . . . . . . . . . .                                                                                                                                                                       |   144 |
|   7.27 | Detection and delineation of P and Q waves . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                           |   145 |
|   7.28 | Detection and delineation of T and S waves .                                                                                                                                                                                                             |   145 |
|   7.29 | . . . . . . . . . . . . . . . . . . . . . . . . . A histogram plot of 10 R peak results detected in 10 channels for an ECG cycle . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . |   146 |
|   7.3  | Delineation result for a lead II heart cycle derived from a 64-channel ECG signal. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                   |   148 |
|   7.31 | Delineation result for a heart cycle measured from a single channel of a 64-channel ECG signal. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                  |   148 |
|   7.32 | Three extracted QRS complexes (row vectors) as an example from the final Signal Extraction Matrix (SEM). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                   |   151 |
|   7.33 | 8000-QRS complex Signal Extracted Matrix (SEM) . . . . . . . . . . . . . . . . . . .                                                                                                                                                                     |   154 |
|   7.34 | Hotelling's T square vector of the signal presented in figure 7.33 . . . . .                                                                                                                                                                             |   155 |
|   7.35 | . . . The result after applying the alignment algorithm on 8000 measured QRS complexes. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                    |   156 |
|   7.36 | The 1 st , the 50 th and the 100 th out of hundred shifted wavelet Meyer functions with 1024 (sample) duration each. . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                 |   157 |
|   7.37 | The result after applying the alignment algorithm on the hundred shifted wavelet Meyer functions. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                    |   157 |
|   7.38 | Alignment of 60-beat QRST complexes from a single-channel ECG signal of an IBT 64-Channel ECG databases from ActiveTwo system. . . . . . . . . .                                                                                                         |   158 |
|   8.1  | T wave morphology variation in an ECG recorded round 6 hours before TDP episode . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                  |   160 |
|   8.2  | The location and the orientation of the human heart in the chest. . . . . . . .                                                                                                                                                                          |   161 |
|   8.3  | Localizing QRS complex onset, R peak and T wave offset for every beat in the whole 24-hour two-channel healthy and TDP tapes. . . . . . . . . . . . . .                                                                                                  |   161 |

|   8.4 | A scatter plot between RR interval and QT interval of a healthy ECG with 80079 beats included. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                | 162        |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
|  8.5  | A scatter plot between RR interval and QT interval of a TDP ECG . . . .                                                                                                                                                                                       | 162        |
|  8.6  | Extracted QRST complexes belonging to the same channel and assembled in one matrix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                      | 163        |
|  8.7  | Aligned QRST complexes to their R peaks . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                                   | 163        |
|  8.8  | Original and its corresponding filtered T waves . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                                   | 164        |
|  8.9  | Aligned QRST complexes after applying low-pass filtering. . . . . . . . . . . . .                                                                                                                                                                             | 164        |
|  8.1  | A submatrix of QRST-complex matrix containing all T waves of one                                                                                                                                                                                              | channel165 |
|  8.11 | An example of the empirical mean raw vector of the data matrix T . . .                                                                                                                                                                                        | 165        |
|  8.12 | . An example of the mean-subtracted data matrix of the original data matrix T . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                   | 166        |
|  8.13 | The first PCA scores (or first RPV) versus T wave beat number. . . . . . . .                                                                                                                                                                                  | 167        |
|  8.14 | The overall measure of variation from a healthy ECG (first channel) . . . .                                                                                                                                                                                   | 174        |
|  8.15 | The overall measure of variation from a healthy ECG (second channel) .                                                                                                                                                                                        | 175        |
|  8.16 | The overall measure of variation from a TDP ECG (before TDP episode)                                                                                                                                                                                          | 176        |
|  8.17 | The overall measure of variation from a TDP ECG (after TDP episode)                                                                                                                                                                                           | 177        |
|  8.18 | The average value of the overall measure of variation for 84 useful channels from the healthy tapes and for 20 useful channels from the TDP tapes.                                                                                                            | 178        |
|  8.19 | The beat-to-beat morphology T-wave variation before and after TDP episode compared to the normal variation level derived from the healthy ECG signals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . | 178        |
|  8.2  | The first two principal Reconstruction Parameter Vectors (RPV) or PCA-scores plot as an example for cluster formation. . . . . . . . . . . . . . . . . .                                                                                                      | 179        |
|  8.21 | Two hundred noisy half-sinus signals from 0 to π with 90 samples each. . 3D scatter plot of the first three PCA scores corresponding to the 200                                                                                                               | 180        |
|  8.22 | input Sinus signals shown in figure 8.21. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                               | 181        |
|  8.23 | Euclidean distance and city block metric. . . . . . . . . . . .                                                                                                                                                                                               | 181        |
|  8.24 | Cluster-Dendrogramm, Figure is adapted from [1] . . . . . . . . . . . . . . . . . . .                                                                                                                                                                         | 182        |
|  8.25 | Clustering result of the figure 8.20. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                                                                         | 182        |
|  8.26 | Clustering result of the figure 8.20 mapped back to real T waves. . .                                                                                                                                                                                         | 183        |
|  8.27 | . . . . A top view of figure 8.26 showing the clustering result mapped back to real T waves. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                            | 183        |
|  9.1  | An example of an input matrix QRS containing all QRS complexes of one channel for a certain 64-channel ECG signal. . . . . . . . . . . . . . . . . . . . .                                                                                                    | 187        |
|  9.2  | An example of the empirical mean of the data matrix QRS presented in figure 9.1. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                  | 187        |
|  9.3  | An example of the mean-subtracted data matrix of the original data matrix QRS presented in figure 9.1. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                          | 188        |
|  9.4  | The energy content for the first three eigenvectors of the mean-subtracted data matrix from the original data matrix QRS presented in figure 9.1.                                                                                                             | 189        |
|  9.5  | The influence of the first principal component, PC1, on the empirical mean raw QRS vector. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                              | 190        |

|   9.6 | The influence of the second principal component, PC2, on the empirical mean raw QRS vector. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                      | 191   |
|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|  9.7  | The influence of the third principal component, PC3, on the empirical mean raw QRS vector. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                       | 191   |
|  9.8  | The first three PCA scores along with the corresponding normalized respiration signal and heart rate signal for one channel of an ECG signal under study. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      | 192   |
|  9.9  | The correlation between the first three PCA scores with both the respiration signal and the heart rate vector in terms of the temporal analysis193                                                                                                                         |       |
|  9.1  | The correlation between the first three PCA scores with both the respiration signal and the heart rate vector in terms of the spatio-temporal analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . | 194   |
|  9.11 | The energy content for the first six eigenvectors, whose cumulative energy content accounts 97.8517% from the whole variance. . . . . . . . . . . . . . . . . . . . .                                                                                                      | 196   |
|  9.12 | The first degree polynomial fitting for the first PCA scores. . . . . . . . . . . . . .                                                                                                                                                                                    | 197   |
|  9.13 | An example of a real QRS complex taken from one of the ECG signals used and its corresponding predicted one. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                                     | 198   |

## List of Tables

| 7.1   | Results obtained from the baseline simulation done on 650 artificial test signals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                              | . 121     |
|-------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| 7.2   | Results obtained from the wavelet-based denoising simulation done on 5580 artificial test noisy ECGs and having values greater than 99% similarity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . | . 126     |
| 7.3   | Validation of the single-channel delineation method, presented in section 7.4.2, on MIT-Arrhythmia database. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                       | . 149     |
| 9.1   | 64-channel IBT measured ECG signals along with their number of beats and channels used in the analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                     | 185       |
| 9.2   | The average value of similarities and errors along the predicted QRS complexes in every channel for each ECG signal, described in section                                                                                                                          | 9.1.2.198 |
| A.1   | The overall measure of variation for 84 useful channels from the healthy tapes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                               | . 201     |
| A.2   | the overall measure of variation before TDP episode for 20 TDP channels from the TDP tapes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                             | 203       |
| A.3   | The overall measure of variation after TDP episode for 20 TDP channels from the TDP tapes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .                                                                                | . 204     |

## Medical Foundations

## 3.1 Heart Anatomy

The human heart is located in the chest between the lungs, behind the sternum and above the diaphragm. It weighs between 200 to 425 grams and is a little larger than the size of a fist [2, 3, 4]. The basis end and the apex end of the heart lie on its main axis which is oriented from the back-top-right to the front-bottom-left of the torso . Everyday it beats in average 100000 times pumping about 7600 liters of blood to the body [5]. Like a sack, a double-layered membrane called the pericardium surrounds the heart. Its outer layer covers the roots of the heart's major blood vessels and is attached by ligaments to the spinal column, diaphragm, and other parts of your body. The inner layer of the pericardium is connected to the heart muscle. The layers are separated by a coating of fluid, letting the heart move as it beats and keeping it attached to the body. The normal periodic contractions and relaxations of the heart allow the human cells receiving the necessary amount of oxygen and nutrients and carrying away their end product of the metabolism.

The walls of the heart are composed of cardiac muscle, Myocardium. It is similar to skeletal muscle, because it has striations. The cardiac muscle consists of four chambers: the right and left atria and ventricles. The anterior aspect of the heart is the right ventricle, whereas the posterior aspect is the left atrium giving the heart its orientation. The endocardium is defined as the thin serous membrane that lines the interior of the heart, whereas the epicardium touches the inner layer of the pericardium that is in actual contact with the surface of the heart. The left ventricle pumps blood to the systemic circulation, where pressure is considerably higher than for the pulmonary circulation, which arises from right ventricular outflow. The left ventricular free wall and the septum is much thicker than the right ventricular wall [6]. The tricuspid valve lays between the right atrium and ventricle, and the mitral valve is between the left atrium and ventricle. Between the right ventricle and the pulmonary artery lies the pulmonary valve, while the aortic valve is in the outflow tract of the left ventricle controlling blood flow to the aorta. Carried in the inferior and superior vena cava, the blood returns from the systemic circulation to the right atrium [7, 8, 9]. First, it has to go through the right ventricle, then it is ejected through the pulmonary valve and the pulmonary artery to the lungs. Oxygen-rich blood returns from the lungs to the left atrium and to the left ventricle. Finally blood is pumped through the aortic valve to the aorta and the systemic circulation. The left and

Figure 3.1. The location and the orientation of the human heart in the chest [6]

<!-- image -->

right coronary arteries branch off the aorta. They are divided afterward into numerous smaller arteries supplying oxygen and nourishments to all heart muscles.

## 3.1.1 Heart Structure

Anatomically, the heart consists of cardiac myocytes, pacemakers and conducting tissues, and extracellular space. Myofibers are connected together by further strands of collagen.

## 3.1.1.1 Cardiac Myocytes

The cell is the basic unit of living tissue. Cells perform different tasks relating to their anatomy and physiology, and exhibit a voltage difference across their membranes. Only nerve and muscle cells are excitable. The working myocardium consists of muscle cells or cardiomyocytes, which have in general a roughly cylindrical shape and are able to produce mechanical tension. The individual contractile muscle cells account more than half of the heart's weight. In atria, they are quite smaller in length and diameter than in ventricles. Each cardiac myocyte is bounded by a complex cell membrane, sarcolemma, separating its intracellular components from the extracellular space.

1. Sarcolemma : The sarcolemma consists mostly of the phospholipid molecules, or socalled phosphoglycerides. Each molecule has a head of a phosphoric acid and a tail of glyceride acid (fatty acid). Since the intercellular and the interstitial media are aqueous, the main construction of a cell membrane consists of two layers of phosphoglycerides where their hydrophilic heads and hydrophobic tails point outside and inside the membrane respectively, figure 3.4. The thickness of the cell membrane

<!-- image -->

Vena

Figure 3.2. Heart chambers, systemic and pulmonary circulations. Figure is adapted from [10]

Figure 3.3. Cut-away diagram of cardiac muscle showing several microfibrils and associated sarcoplasmic reticulum and the sarcolemma and t-tubular systems [11]

<!-- image -->

ranges between 4 and 5 nm [12] and contains also various and specific proteins forming macromolecular pores and enabling ionic and metabolic transportation outwards

and inwards the cell. These proteins are specified mainly by the type of ions which can pass through and their functions vary between ionic transporting, ionic exchanging or ionic pumping mechanisms, e.g. the sodium channel, the potassium channels, the calcium channels, the sodium-calcium exchanger and the sodium-potassium pump. They are therefore responsible of the selective sarcolemmal permeability to ion types. Several gene-coded subunits, i.e. alpha , beta and gamma , contribute effectively in forming the molecular structure of a voltage-gated channel and furthermore in modulating its electrophysiologic properties and functions. In the cardiac myocytes, there is mainly one kind of sodium channel, two types of calcium channels [13, 14, 15, 16] and large variety of potassium channels [17, 18, 19, 20]. Calcium channels can be divided into L-type calcium channels or so called dihydropyridine receptors (DHPR) and T-type calcium channels. Whereas, potassium channels can be classified under two classes, 2TM-1P channels with two transmembrane segments and one pore in between and 6TM-1P channel with six transmembrane segments and one pore in between. In some places, the cell membrane invaginates forming an extensive tubular network (T-tubules) which connects the intracellular space with the extracellular one. The adjacent cells are connected and glued together mechanically by means of intercalated discs of specialized proteins called connexins [21, 22]. Having bundles shape, these proteins are located near to the ends of cardiac myocytes [23]. They form low resistance intercellular channels. These pores between the cells are called gap junctions [21, 22, 24, 25]. Gap junctions allow the passage of intracellular metabolic products, anions and cations between cells showing no kind of ion selectivity. The conductance of the gap junctions is influenced by the intracellular ion concentration of H + , Ca 2+ , Na + , and Mg 2+ , drugs, extracellular pH value, the genetic expression of connexins and the trans-junctional voltage [26, 27, 28, 29].

Figure 3.4. The typical structure of the sarcolemma and the voltage-gated ion channel. Figure is adapted from [6]

<!-- image -->

Figure 3.5. Structure of a typical voltage-gated ion channel: (a) The α subunit of a typical voltage-gated ion channel comprises four subunits [homologous subunits for potassium ions (K + ) channels or homologous repeat domains for sodium ion (Na + ) and calcium ion Ca 2+ channels]. Each domain or subunit is made up of six transmembrane domains (S1S6); the S4 domain is charged and acts as a voltage sensor. Cations pass through the aqueous pore between the four subunits into the cell. (b) The assembled ion channel has one a subunit plus other auxiliary subunits (b, d, etc.) that modulate channel function. Mutations in K + and Na + voltage-gated ion channels are associated with human epilepsies; mutations in Ca 2+ voltage-gated ion channels are associated with mouse models of spike-wave epilepsies. The figure has been modified from [30]

<!-- image -->

.

2. Intracellular Components : The cardiomyocyte contains one nucleus or several nuclei, mitochondria, a sacroplasmic reticulum and many rod-like bundles of myofibrils. A liquid solution, so-called cytosol, of carbon hydrates, salts, lipids and proteins fills up the rest of the volume of the intracellular space. The centrally-located nucleus contains almost all genetic information of the cell. Located between sarcolemma and myofibrils, many mitochondria are responsible to transfer chemical energy into ATP needed to maintain the heart's function and viability. This energy is actually produced by the ribosomes inside the mitochondria in the form of adenosine triphosphate (ATP). Microscopically, each myofibril consists of many anisotropic bands with high birefringence, namely the A-band, and isotropic bands with low birefringence, the I-band.

The Z-disk, also called Z-line, a dense staining band, bisects every I-Band. Thus, a sacromere is defined as the segment between two successive Z-discs. It consists of thick myosin filaments and thin actin, troponin and tropomyosin filaments. The physical process of contraction is realized by the displacement of the thin filaments along the thick filaments with the help of the contractile proteins (actin &amp; myosin) and the regulatory proteins (troponin &amp; tropomyosin). The H-zone is located in the center of each A-band, where there is myosin available. Every H-zone contains another dark-protein region in its center, called M-line.

Figure 3.6. The structure of a sacromere: the actin filaments are the major component of the I-band and extend into the A-band. Myosin filaments extend throughout the A-band and are thought to overlap in the M-band. The giant protein titin (connectin) extends from the Z-line of the sarcomere, where it binds to the thin filament system, to the M-band, where it is thought to interact with the thick filaments. Figure is adapted from [31]

<!-- image -->

The main function of the Sacroplasmic Reticulum (SR) is to regulate the intracellular movements of calcium ions, that is, releasing calcium to the myofilaments in order to establish a cardiac contraction and retrieving calcium back from them to decrease the cytosolic calcium ion concentration and facilitate relaxation. Furthermore, the SR plays an important role in the interaction between regulatory proteins and contractile mechanism determining the force of cardiac contraction.

## 3.1.1.2 Pacemakers and Conducting Tissues

Certain cells of the heart have the ability to undergo spontaneous depolarization, socalled automaticity. They are located in the sinoatrial node, SA or sinus node, in the right atrium at the superior vena cave. These cells are also called pacemaker cells in the way they are able to generate an action potential without any influence from other cells and in the way their discharge determines the rate of the heart. Their self-extracting action is actually controlled by sympathetic and parasympathetic autonomic nervous systems. The sympathetic system dominates a high heart rate during activity, exercise and stress, whereas the parasympathetic system maintains much lower heart rate during relaxation. After the electrical wavefront is generated from SA, it propagates through both atria and

Figure 3.7. The structure of the thick and thin filaments [32]

<!-- image -->

reaches the atrioventricular node (AV node), which is located at the boundary between the atria and ventricles. The AV node provides the only conducting path from the atria to the ventricles in a normal heart [6]. Moreover, it collects and delays the electrical impulse before entering into the ventricles and allowing the atrial contraction to further increase the blood volume in the ventricles before ventricular contraction occurs [33]. The propagation from the AV node to both ventricles is performed by the ventricular conduction system. Located in the wall between the two ventricles, the bundle of His, also called atrioventricular bundle, is the first component in that system, through which the electrical propagation enters the ventricles. The pathway is then divided into rapidly conducting bundles along each side of the septum with branches to the left and right ventricles. The left bundle subsequently divides into an anterior and posterior branch [6]. The system ramifies further into an extensive network of specialized conduction fibers called Purkinje fibers diverging to the inner sides of the ventricular walls.

## 3.1.1.3 Vascular System and Extracellular Space

The coronary arteries, veins, and many small blood vessels, called capillaries occupy about the half of the exctracellular space. The capillaries lie very close to the surface of more than one third of the cardiac cells allowing diffusion of nutrients and oxygen into the cells and facilitating the removal of metabolic waste products. The other half of the extracellular space is filled with interstitial fluid. By means of the T-tubular system, this fluid is able to enter into the cell. In contrast to the cytosol, the extracellular cell-bathing fluid is rich in sodium and low in potassium.

## 3.1.2 Myofiber Orientation of Cardiac Muscle

The cardiac myofibers consist of groups of myocytes surrounded by collagen weaves. The orientation of these myofibers in the heart plays a strong role in generating anisotropic

Figure 3.8. The conduction system of the heart [6]

<!-- image -->

electrical excitation and mechanical contraction. The majority of the working cardiac fibers in atria have a very complex orientation. In contrast the fiber of the working ventricular fibers show better organization with continuously transmural rotation and spiral orientation.

## 3.2 Electrophysiology of the Heart

## 3.2.1 Resting Voltage, Action Potential and Refractory Periods of a Single Cell of Working Myocardium

## 3.2.1.1 The Resting Voltage

Like all living cells at rest, the cardiac muscle cell (myocyte) is polarized, so that the potential inside the cell (intracellular space) is negative with respect to the outside (interstitial space). The transmembrane potential is defined as the potential difference across the surface membrane of the cell. It is controlled primarily by three factors. The first is the concentration of ions on the inside and outside of the cell, particularly Na + , K + , Cl -, and Ca 2+ . The second factor is the permeability of the cell membrane to those ions through specific ion channels. The last factor is the activity of electrogenic pumps (e.g., Na + /K + -ATPase and Ca 2+ transport pumps) that maintain the ion concentrations across the cell membrane.

Figure 3.9. The cardiac fiber orientation for the heart demonstrated on the heart of the Visible Man, Figure is adapted from [34]

<!-- image -->

Because K + concentration is high inside the cell and low outside, a chemical gradient for K + to diffuse out of the cell is found. In opposite, Na + and Ca 2+ chemical gradients for an inward diffusion are found. The natural tendency of sodium and potassium ions is to diffuse across their chemical gradients to attempt to reach their respective equilibrium potentials, with sodium diffusing into the cell and potassium diffusing out. However, the resting cell membrane is approximately 100 times more permeable to potassium than to sodium, so that more potassium diffuses out of the cell than sodium diffuses in. This permeability to potassium is due to potassium channels that are open at the resting voltage. As a result, the dominant outward leak of potassium ions produces a polarizing current that establishes the cell's resting potential of roughly -70 mV [35].

## 3.2.1.2 The Action Potential of a Single Cell of Working Myocardium

By applying an external stimulus, cells of excitable tissues can be depolarized. An action potential can be produced by a sequence of influx and outflux of multiple cations and anions through the cell membrane. Once a cardiac cell is getting excited, an electrical stimulation to the cells that lie adjacent to it and furthermore to all the cells of the heart will be propagated [36]. The action potential has five phases, numbered from zero to four. Atypical action potential for a cardiac myocyte in the left ventricle is shown in figure 3.10.

Figure 3.10. The Action Potential of a single cell of working Myocardium. Figure is adapted from [37].

<!-- image -->

Phase 4 represents the resting transmembrane potential, in other words, this voltage can be measured if the cell is not stimulated. This phase of the action potential is associated with the diastole of heart chambers. Phase 0 is known as the rapid depolarization phase. The maximum rate of depolarization of the cell, dV max /dt , is determined by the slop of curve corresponding to this phase. This phase is associated with opening of the fast Na + channels, rapidly increasing the membrane conductance to Na + (gNa) and a rapid influx of Na + ionic current (INa) into the cell. In fact, the fast sodium channel has two gates, the h gate and m gate, whose interaction allows Na + to enter the cell through this channel. At rest, the m gate is closed and h gate is open, but when the transmembrane potential approaches a threshold (about -60 mV), the m gate opens quickly while the h gate closes slowly. After a very short time, both gates will be open changing the sign of the transmembrane voltage to positive value (round +20 mV), to the so-called overshoot. The closure of the fast Na + channel after a short time and the slower outflow of potassium through the potassium channels are tending to restore the initial state of the membrane generating the phase 1. The balance between inward movement of Ca 2+ (ICa) through Ltype calcium channels and outward movement of K + through potassium channels sustains the phase 2 (or so-called plateau) of the action potential. Cardiac myocytes have different characteristics of the plateau phase. During this phase the fast sodium channels are not active keeping the cell immune to any external stimulus. Therefore, it is called refractory period. In the phase 3 of the action potential, K + will be accumulated in the extracellular space leaving the intracellular space. This action is responsible for the repolarization of the cell. The cell can be depolarized again in this period by very large stimuli, therefore it is called refractory relative period. Finally, K + channels close when the transmembrane potential is set back to the resting phase and the initial concentration of ions is rapidly restored by means of Na-K pumps and Na-Ca exchangers. The myocytes throughout the heart have different time course of action potentials figure 3.11.

Figure 3.11. The resting voltage and action potential electrophysiology of a single cell of working Myocardium. Figure is adapted from [6]

<!-- image -->

## 3.2.2 Excitation Propagation and Cardiac Contractions

Cardiomyocytes consist of three systems: (1) a sarcolemmal excitation system that participates in spread of action potential (AP) and functions as a switch initiating intracellular events giving rise to contraction, (2) an intracellular excitation-contraction coupling (ECC) that converts the electric excitation signal to a chemical signal and activates the (3) contractile system, a molecular motor based on formation of chemical bridges between actin and myosin.

1. The Excitation System : This system is responsible to maintain the resting potential, create an action potential and facilitate spreading the AP. The cardiac cycle is initiated from the excitation system of SA node. The rapid change in the voltage during an AP causes the activation in the excitation system. Consequently, the neighboring cells will be depolarized. As a result, an electrical impulse, also called the cardiac electrical wavefront, propagates through the conduction system of the heart and spreads from cell to cell throughout the myocardium in the way that the atrial and ventricular contraction (depolarization) and relaxation (repolarization) will happen with the correct timing in the healthy heart [33].
2. The Excitation-Contraction Coupling System : Excitation-contraction coupling (ECC) is established by the sarcotubular system, an arrangement of specialized sar-

Figure 3.12. Schematic diagram of the major cellular components involved in contraction of the myocyte. Figure is adapted from [38].

<!-- image -->

colemmal and intracellular membranes that controls and amplifies the ability of AP to switch the contractile system on and off by creating electrochemical signals between the sarcolemma and intracellular organelles [39]. When a myocyte is depolarized by an AP, calcium ions enter the cell during phase 2 of the action potential through L-type calcium channels triggering a subsequent release of calcium that is stored in the sarcoplasmic reticulum (SR) increasing the intracellular calcium concentration from about 10 -7 to 10 -5 M. The released calcium binds to troponin-C (TN-C) that is part of the regulatory complex attached to the thin filaments. When calcium binds to the TN-C, this induces a conformational change in the regulatory complex such that troponin-I (TN-I) exposes a site on the actin molecule that is able to bind to the myosin ATPase located on the myosin head. This binding results in ATP hydrolysis that supplies energy for a conformational change to occur in the actin-myosin complex [38].

3. The Contractile System : The building block of the contractile system is the sarcomare. The result of the changes made by the released calcium in ECC is a movement between the myosin heads and the actin. The actin and myosin filaments slide past each other thereby shortening the sarcomere length. This ratcheting cycle occurs as long as the cytosolic calcium remains elevated. At the end of phase 2 of AP, calcium entry into the cell slows down lowering the cytosolic calcium concentration. Cytosolic calcium is transported out of the cell by the sodium-calcium-exchange pump. This

Figure 3.13. The Genesis of Electrocardiogram: the waveform and timing of different action potentials from different regions and specialized cells of the heart and the corresponding cardiac cycle of the ECG as measured on the body surface. Figure is adapted from [6]

<!-- image -->

cycle ends when new ATP binds to the myosin head, displacing the ADP, and the initial sarcomere length is restored.

## 3.2.3 The Generation of an Electrocardiogram and the Dominant Cardiac Vector

The Electrocardiogram (ECG) represents a temporal and spatial summation of the extracellular fields of the action potentials generated by millions of cardiac cell. It describes the different electrical phases of the cardiac cycle. ECG provides a measure of the electrical currents generated in the extracellular fluid by the changes in the APs, figure 3.13. At any given instant, only a group of cells out of millions of individual cells in the myocardium depolarizes simultaneously. They can be represented as an equivalent current dipole source to which a vector is associated, describing the dipole's time-varying position, orientation, and magnitude [33]. The dominant vector describing the main direction of the electrical wavefront can be defined as a summation of the vectors of all current dipoles in the heart at a certain time instant.

## 3.3 ECG Lead Systems

The electrical activity of the heart can be characterized by measurements acquired from the cardiac cellular level (invasive) as well as from the body surface (non-invasive). Due to the fact that this work is based on analysing the Electrocardiogram recorded from electrodes placed on different parts of the body, only non-invasive ECG lead systems are presented.

## 3.3.1 The Conventional 12-lead System

## 3.3.1.1 Bipolar Limb Leads

In the year 1913, Einthoven et al. developed a method of studying the electrical activity of the heart by representing it graphically in a two-dimensional geometric figure, namely, an equilateral triangle [40, 41]. Einthoven's hypothesis is based on several oversimplifying assumptions [41]: (1) the body is a homogeneous volume conductor. (2) The mean of all electrical forces can be considered as originating in an imaginary dipole located in the electrical center of the heart. (3) Electrodes placed on the right arm (RA), left arm (LA) and left leg (LL) are used to pick up the potential variations on these extremities to form an equilateral triangle, also called Einthoven's triangle. In fact, the latter is not a true geometric equilateral or equiangular triangle, but because the distances from the dipole to the extremities are great enough to approach 'infinity', the extremities do form an equilateral triangle indeed. The three bipolar limb leads are denoted I , II , and III and are obtained by measuring the voltage difference between RA, LA, and LL in the following combinations:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where φ LA , φ RA and φ LL denote the electric potential recorded on the LA, RA and LL, respectively. The limb leads describe the cardiac electrical activity in three different directions of the frontal plane. In that case, each direction is separated by an angle of 60 o , figure 3.18.

Wilson Central Terminal (WCT) is defined as a common point, where the limb leads are connected together, through three resistors of 5000 ( Ω ) each. The potential of φ WCT remains almost constant throughout the entire cardiac cycle with respect to the potential zero at the infinity. WCT is calculated as follows:

<!-- formula-not-decoded -->

Figure 3.14. Einthoven limb leads and Einthoven triangle. Figure is adapted from [42]

<!-- image -->

Figure 3.15 shows the generation of the ECG signal in the Einthoven limb leads along with the time-variant cardiac dominant vector and its projections on each of the three Einthoven limb leads.

## 3.3.1.2 Augmented Unipolar Extremity Leads

The main aim of these leads is to fill the 60 o gaps in the directions of the bipolar limb leads. That is, the augmented limb leads, namely aV R, aV L, and aV F , describe directions which are shifted 30 o from those of the bipolar limb leads [42], figure 3.18 . They are defined as the differences between one corner of Einthoven's triangle and the average of the remaining two corners, figure 3.16 :

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Theoretically, Lead III as well as the augmented unipolar limb leads do not need to be recorded, but instead they can be computed from Lead I and Lead II.

Figure 3.15. The generation of the ECG signal in the Einthoven limb leads. Figures are adapted and adjusted from [6]

<!-- image -->

## 3.3.1.3 Unipolar Precordial Leads

The unipolar precordial ECG is obtained by placing the exploring electrodes connected to the positive pole of the ECG amplifier on the six locations of the anterior and left portions of the chest [41], see figure 3.17(a). WCT is used in this case as the indifferent electrode, see figure 3.17(b). The Unipolar Precordial Leads are called also Wilson Unipolar Chest Leads. The main six precordial leads are called V 1 ...V 6 . They yield a positive deflection when facing positive charges and negative when facing negative charges according to what Wilson called the the solid-angle concept [41]. This concept is merely an imaginary cone, which extends from the side in the chest throughout the heart, so that a precordial electrode is at its apex and the opposite epicardial surface at its base [41]. According to Wilson's scalar concept of ECG, the solid angle subtended by the corresponding lead

Figure 3.16. The Augmented Unipolar Limb Leads, aV R, aV L, and aV F . Figure is adapted and adjusted from [6]

<!-- image -->

Figure 3.17. The unipolar precordial leads: a) The main electrode locations in Wilson chest leads defined anatomically b) Recording the unipolar precordial leads. Figures are adapted from [6].

<!-- image -->

records the electrical activity from the regions of the heart over which the lead is placed as well as distant regions [41]. Leads V 1 and V 2 record the activity of the right ventricle. Whereas leads V 3 and V 4 reflect the activity of the anterior wall of the left ventricle and leads V 5 and V 6 view the lateral wall of the left ventricle.

Figure 3.18. The direction of the bipolar limb leads and the augmented limb leads in the frontal plane and the precordial leads in the transversal plane: a) The direction of the bipolar limb leads and the augmented limb leads in the frontal plane. b) The direction of the precordial leads in the transversal plane. Figure are adapted from [33].

<!-- image -->

## 3.3.1.4 Mason and Likar Lead System

In 1966, Mason and Likar published their recommendations for moving the limb electrodes used to record the 12-lead ECG from the limbs to the thorax [43] for exercise electrocardiography. Their repositioned electrodes are shown in figure 3.19. They compared ECG recordings where the right and left arm electrodes were positioned in the

Figure 3.19. The modified electrode positions for the limbs according to Mason and Likar [43] . Figure is adapted from [46]

<!-- image -->

conventional areas of the arm to those obtained from gradually moving the electrodes to progressively proximal positions up the arms and then over the upper anterior chest. Finally, it was recommended that the right arm electrode be moved to a point in the infraclavicular fossa medial to the border of the deltoid muscle and 2 cm below the lower border of the clavicle. The corresponding position was recommended for the left arm electrode as shown in figure 3.19. Further experimentation led to a recommendation that the left leg electrode (denoted LL) be placed in the anterior axillary line halfway between the costal margin and the iliac crest. They suggested that the location of this electrode was not critical; that is, it could be varied by a few centimeters in any direction to avoid skin folds, and so on. Some authors simply consider this reference point as being the left iliac crest [44]. Mason and Likar initially illustrated the right leg electrode as being on the right thigh, but for convenience it is now a matter of routine to place this electrode in the region of the right iliac fossa as recommended by the American College of Cardiology [45, 46].

## 3.3.2 The Corrected Orthogonal Leads

This lead system is known also as Frank lead system. Seven electrodes placed on the chest, back, neck and left foot are used to view the heart from the left side, from below and from the front. This kind of lead system reflects the electrical activity in the three perpendicular directions X, Y, and Z and traces out a three-dimensional loop for every cardiac cycle by

means of the time-variant cardiac dominant vector. The three projections of this loop onto XY, XZ and YZ planes are also recorded. The morphology of the loops, their direction of rotation and their areas are the main spatial quantities that improve ECG-based diagnosis of some cardiac pathologies, like myocardial infarction. This particular type of recording is referred to as a vectorcardiogram (VCG).

## 3.3.3 Body-Surface Mapping Lead Systems

Body-surface potential mapping, also called multichannel electrocardiography, is an extension of conventional electrocardiography aiming for refining the noninvasive characterization and use of cardiac generated potentials [1-5]. By increasing the spatial sampling of body-surface electrocardiographic information, the latter characterization is improved. The single electrocardiographic lead provides only a simple means for detecting clinically significant cardiac pathologies. Multichannel ECG mapping, on the other hand, provides the spatial ECG information which, on a theoretical basis, provides for identification of localized cardiac activity and hence the opportunity for improving the utility of ECG in clinical care of patients. A body-surface potential map (BSPM) may be defined as the temporal sequence of potential distributions observed on the thorax throughout one or more electrical cardiac cycles. In practice, tens or hundreds of unipolar ECGs are recorded, either simultaneously or individually with subsequent time alignment. For each time instant of interest, the potential measured in each lead is associated with the spatial location at which it was measured. The spatial distribution of the set of potentials at a particular instant in the cardiac cycle may then be displayed as isopotential contour maps showing lines which connect all sites which have the same potential [46], figure 3.20. Body-surface mapping was actually developed for two reasons. The first one was to permit a study of the spread of excitation over the thorax. This allowed the normal patterns to be studied and inferences drawn on the time of epicardial 'breakthrough' of activation at the right and left ventricles. Some investigators use between 16 and 240 electrodes to map the thorax using computer techniques for plotting. The second reason for mapping is to assess in a mathematical way the total electrical information available [46]. Barr suggested [48] that 24 surface leads would allow the thorax to be mapped so that with the use of a transformation, the ECG data at other points could be estimated. The aim behind this particular study was to derive information on the equivalent cardiac generator and so attack the inverse problem [46]. Kornreich used a 126-lead system to map the body surface and from this concluded that nine independent leads would be adequate to retrieve all of the clinically useful information on the body surface [49]. The group of Taccardi used a 219 irregularly spaced electrode array [50]. Lux et al. [51] also utilized complex mathematical techniques to reduce the number of electrodes required for mapping to a more limited number on which they were able to calculate normal ranges and assess the results of exercise testing. Mapping Systems used for clinical purposes, such as detecting areas of ST elevation following acute myocardial infarction, generally consist of a small array of unipolar chest leads. Maroko et al. in 1972 [52] suggested the use of a 5x7 electrode array for ST mapping following myocardial infarction. In 1979, Fox et al. [53] utilized a 4x4 array of electrodes for mapping infarction and also for exercise testing. It was subsequently suggested that this be reduced to a 4 x 3 array [54]. Monro et al. [55] employed a 24-electrode array that mapped both the anterior and posterior chest walls.

Figure 3.20. (a) Electrodes of the Amsterdam 62-lead body surface mapping set indicated with solid circles and including the standard 6 precordial electrodes illustrated with open circles. (b) Example of a body surface potential map recorded with the lead set shown in panel (a). This map displays the potential distribution, integrated over some time interval, over the body surface, using contour lines which connect points with equal values. Plus and minus signs indicate the extrema positions; the shaded area identifies torso sites with positive values [47]. Figures are adapted from [47]

<!-- image -->

By the means of sophisticated mathematical interpolation methods, the potentials at any other point on the thorax could be calculated [56, 57].

## 3.3.4 Ambulatory Monitoring Leads

Ambulatory ECG monitoring is used to identify patients with transient symptoms, e.g., palpitations, light-headedness, or syncope, which are indicative of arrhythmias. Another group of patients are those at high risk of sudden death after infarction. Ambulatory monitoring is also used in patients who are on antiarrhythmic drugs and whose reaction to the therapy needs to be assessed. The ambulatory ECG recording technique is also called Holter monitoring after its inventor Norman Holter who introduced the first portable (analog) device to record an ECG in the late 1950s [58]. Ambulatory ECG signal is

Figure 3.21. The recommended electrode positions for two-channel ambulatory ECG recording according to the Committee on Electrocardiography of in the American Heart Association [44]. A+ and A- are the positive and negative electrodes for the V5 type lead (not the same as V5 in precordial wilson chest leads) and B+ and Bare the electrodes for the Vl type lead. The open circle denotes an electrode on the back. Figure is adapted and adjusted from [46]

<!-- image -->

recorded during 24 hours or more of normal daily activities for the patient [46]. The Committee on Electrocardiography in The American Heart Association (AHA) suggest for electrode placement for two-channel recording [59]. It is based on a five-electrode System, one of which is a ground electrode with the other two pairs each forming a bipolar lead. The recommended electrode positions are as follows. (a) V1 type lead. The positive electrode should be in the fourth right intercostal space, 25 mm from the sternal margin while the negative electrode should be in the lateral third of the left infraclavicular fossa. (b) V5 type lead. The positive electrode should be in the fifth left intercostal space at the anterior axillary line and the negative electrode should be 25 mm below the inferior angle of the right scapula on the posterior torso [46]. The fifth electrode, the ground electrode, should be placed in the lateral third of the right infraclavicular fossa. The electrode positions are illustrated in figure 3.21.

For several years, much emphasis was placed on developing algorithms for classification of beat morphologies since it was believed that the VPB count per hour represented an important risk factor in sudden death. Although it was later shown that this belief was unfounded, VPB detection remains an essential part of the analysis of ambulatory ECGs. For example, it is necessary to deal with the presence of ectopic beats when an EGG is analyzed with respect to heart rate variability. The latter type of analysis in Holter monitoring has shown great promise in predicting mortality rates in patients after myocardial infarction [33]. A second reason for undertaking ambulatory electrocardiography may be to evaluate Symptoms that are possibly related to myocardial ischemia, i.e. assessing ST-segment changes. The AHA committee noted previous suggestions that a pair of leads approximating V3 and aVF from the 12-lead ECG may detect more ST-segment shifts in patients with unstable angina [60]. In another study [61], Quyyumi et al. utilized two

Figure 3.22. Schematic diagram of normal sinus rhythm for a human heart as seen on ECG. Figure is adapted from [6]

<!-- image -->

bipolar leads to assess ST changes in patients with varying severity of coronary artery disease. Diagnosis of atrial arrhythmias using the ambulatory EGG is rendered difficult by the fact that P waves are frequently masked by noise and artifacts. As a result of this, it is extremely difficult to design algorithms for P wave detection that give a reliable diagnosis [33].

## 3.4 The Normal ECG Waves, Time Intervals, and its Normal Variants

The normal ECG signal represents a normal cardiac cycle. Figure 3.22 illustrates the normal ECG of one cardiac cycle along with its components. The normal variances and characteristics of its waves, durations and time intervals are described as follows:

## 3.4.1 The P Wave

Depolarization in the atria is registered as the P wave in the ECG. Duration of the P wave should not exceed 0.10 sec in limb leads, or 0.12 sec in chest leads. Its amplitude averages 0.1-0.3 mV. P wave is normally positive in limb leads except in aVR lead, where it is always negative. It is most pronounced in lead II. P wave is always positive in left precordial leads,

Figure 3.23. The power spectrum of the P wave, QRS Complex and T wave: This plot gives approximately the normal variation of the ECG spectral components. Larger variation can exist depending on lead position, ECG morphology and subjects. Figure is adapted from [33]

<!-- image -->

often biphasic (+ -) over the right chest wall. The autonomic nervous system activity plays a considerable role in the variation of P wave morphology. The amplitude of P wave may increase remarkably, above all in leads II, III and aVF, when the sympathetic tone is increased. On the other hand, when there is an increased parasympathetic tone, P wave becomes flat in leads II, III, and aVF. The spectral characteristics of a normal P wave is usually considered to be low-frequency, below 10-15 Hz [33], figure 3.23.

## 3.4.2 The QRS Complex

The ventricular complex represents the initial ventricular depolarization. It usually comprises a Q, R and an S wave. Every positive wave is called R. The first negative wave preceding an R is always called Q and the first negative wave following R is always called S. A possible second or third R wave is called R' or R', figure 3.24. It is also preferable to speak of a split ventricular complex, when several waves are presented. Notation of individual waves of the ventricular complex is different according to amplitude by using small or large letters. The relation of the waves to each other will be the measure for 'small' or 'large', since there is no absolute measure for that. QRS complex is mostly high concentrated between 10-50 Hz, figure 3.23.

Figure 3.24. Different morphologies of QRS complex. Figure is adapted from [62]

<!-- image -->

## 3.4.3 The PR or PQ Interval

It is measured from the start of the P wave to the start of ventricular complex. It should not be shorter than 0.12 sec , nor longer than 0.20 sec . Prolonged AV conduction time at the rest which becomes normal on exercise is not necessarily a sign of abnormality.

## 3.4.4 The T Wave

It expresses repolarization of the ventricles. Its amplitude must always be taken in relation to the R wave. T wave is always positive in lead I and II, and it is always negative in aVR lead.

## 3.4.5 The U Wave

After T wave, an ECG can sometimes show a U Wave. It is of the same deflection as T Wave and similar to shape to P Wave. The U Wave is thought to represent late repolarization of the Purkinje fibers in the ventricles [63].

## 3.4.6 The PP Interval and the RR Interval

PP interval is defined as the duration of atrial cycle. It is useful as an indicator of atrial rate. Whereas, RR interval is defined as the distance in msec between two successive R waves. It is an indicator of ventricular rate representing the length of a ventricular cardiac cycle. Moreover it is very important to characterize different arrhythmias and to study the heart rate variability.

## 3.4.7 The QT Interval

Referring to Lepeschkin and Surawicz, this interval is measured from the beginning of Q wave (if this is absent, from the beginning of R wave) to the end of the T wave as it returns to the isoelectric line [40]. Its duration depends on the heart rate. In some cases, determination of QT interval (Q onset, T end or both) is difficult. One of these cases is the hypokalemia, where flattening of T wave is increased and accompanied by the U wave. In that case, QU interval needs to be considered instead of QT interval. Although this interval has been considered as a surrogate of action potential duration, it yields a limited view of the complicated electrogenesis of the ventricular repolarization [64]. Nevertheless, the most important aspect of this interval is its relation with heart rate [64]. On first sight, the task of describing the QT/RR relationship does not appear to be too complicated. Unfortunately the problem is far from simple [65]. The standard clinical correction is Bazett's formula [66] calculating the heart rate corrected QT interval, QT c . Bazett's formula is

<!-- formula-not-decoded -->

where QT is the QT interval measured in msec and RR is the interval from R peak of one QRS complex to R peak of the next QRS complex, measured in seconds. However, this formula tends to not be accurate, and over-corrects at high heart rates and under-corrects at low heart rates.

In fact, the adjustment of the QT interval to changes in rate does not occur immediately but rather gradually. In normal subjects and even in persons with minimal myocardial abnormalities, abrupt RR changes do not prolong the QT interval if the pauses are short [39]. Longer pauses produce some prolongation but restitution tends to occur in the first postpause beat [64]. This behavior can be considered as a type of cardiac memory, since QT interval is influenced by the past history [67]. The differences between the longest and the shortest QT intervals of the 12-lead ECG is defined as QT dispersion, QT d . It has emerged as a noninvasive measurement for quantifying the degree of myocardial repolarization inhomogeneity [68]. Some other authors, do not accept this interpretation and they claimed that the width of the T wave is in fact a direct measure for the repolarization inhomogeneity when T onset is clearly visible [69]. QT d can also be noticed from the abnormal morphology of T-Loop in VCG. QT dispersion has been linked as a risk indicator for arrhythmic cardiac death in many chronic cardiac pathological cases.

## 3.4.8 The ST Segment

ST segment represents the period from the end of ventricular depolarization to the beginning of ventricular repolarization. The ST segment lies between the end of the QRS complex and the initial deflection of the T-wave and is normally isoelectric. It is clinically important if it is elevated or depressed as it can be a sign of ischemia and hyperkalemia [70]. In order to interpret ST segment correctly, the J point should be localized precisely. The J point, as definition, is the time instant in the ECG when the QRS complex curves into the ST segment.

Figure 3.25. The premature ventricular contraction (PVC). Figure is adapted from [75].

<!-- image -->

## 3.5 Heart Rhythms and Arrhythmias

The electrical impulses generated in the SA node control the rhythm of the heart. Any disturbance of the normal sinus rhythm is called arrhythmia. In general, arrhythmia may occur in the heart either when depolarization is initiated by other pacemaker cells exhibiting accelerated automaticity as compared to the SA node, or when the conduction of the electrical impulses is altered, that is, when the conduction of the cardiac cells is partially or completely blocked causing a propagation delay of the impulse or conduction failure [71, 72, 33]. Arrhythmia can be classified regarding the site of its origin.

## 3.5.1 Sinus Rhythm

SA node is the original source for the normal sinus rhythm with a rate between 50 and 100 beats per minute at rest. Sinus bradycardia and sinus tachycardia are defined as a rhythm below 50 and above 100 respectively. The heart rate is influenced by external perturbations like physical and mental stress and it is influenced by the continual variation of the balance between the parasympathetic and the sympathetic activities of the autonomic nervous system. Numerous studies on analysing the dynamics of spontaneous heart rate variability has been done during the recent years. This research aimed for diagnosing and predicting cardiovascular diseases and life-threatening arrhythmias [73, 74].

## 3.5.2 Premature Beats

The normal sinus rhythm is sometimes interrupted by a beat occurring before the expected time of the next sinus beat and is therefore referred to as a premature beat. In addition the terms 'ectopic beat' and 'extrasystole' are frequently used synonyms [33]. When the ectopic beat is originated from the atria, it is called supraventricular premature beat (SVPB) and when its origin is from the ventricles, it is called ventricular premature beat (VPB). Ventricular premature beats, also known as premature ventricular contraction (PVC) or heart palpitations, are characterized by a premature broad QRS complex with duration greater than 120 msec, and without preceding P wave, see figure 3.25.

Bigeminy, Trigeminy and Quadrigeminy are defined as every normal beat is followed by one, two and three premature beats respectively, see figure 3.26 as an example of Bigeminy. Whereas, if a premature beat occurs after one, two, or three normal beats, they will be defined as (1:1 extrasystole), (2:1 extrasystole) and (3:1 extrasystole) respectively. Two consecutive VPBs are called a couplet, see figure 3.27; three consecutive VPBs are called a triplet. Three or more consecutive VPBs are called a salvos or ventricular tachycardia.

Figure 3.26. An example of Bigeminy. Figure is adapted from [75].

<!-- image -->

Figure 3.27. An example of Couplet. Figure is adapted from [75].

<!-- image -->

In VPBs the ventricular impulses are conducted retrogradely to the atria, at least partially. Therefore about 50% of them are discharging the sinus node. Monomorphic VPBs are called also unifocal because they generate from the same focus. Whereas, Polymorphic VPBs generate from the several focus. Most of the VPBs have a right bundle-branch block (RBBB)-like pattern or right bundle-branch block (RBBB)-like pattern.

## 3.5.3 Atrial Arrhythmia

One or multiple atrial ectopic foci are responsible for many of the various rhythm disturbances causing atrial arrhythmias. If the ectopic focus is located between SA node and AV node, the P wave will be abnormal and sometimes negative in the ECG. When the ectopic focus is located near to the AV node the atria and the ventricles will be depolarized at the same time making P wave coincide with QRS complex in the ECG.

## 3.5.3.1 Atrial Tachycardia

Increasing the automacity in the pacemaking cells of one or multiple foci within the atria, atrial tachycardia will increase the heart rate. The P wave sometimes appears in the ECG coinciding with the previous T wave or even the previous QRS complex [33].

## 3.5.3.2 Atrial Flutter and Atrial Fibrillation

In these kinds of atrial tachyarrhythmias, the atria and the ventricles are not synchronized. The cause of both arrhythmias is a continuous reentry of an electrical impulse in the atria. The reentry mechanism starts when an impulse depolarizes receptive myocytes neighbouring an area of relatively longer refractory periods. When the originally inactive area becomes activated, the impulse may propagate back towards the area which was initially depolarized. If the latter has had time to recover and to depolarize again, the

Figure 3.28. a) Atrial flutter. a) Atrial fibrillation. Figures are adapted from [75].

<!-- image -->

reentry circle will be repeated. The high rate of atrial contraction will lead to a slow blood inflow through the atria increasing the chance for a clot to be produced [33]. The clot afterwards might cause a stroke or severe damage to any other part of the body. In case of atrial flutter, the atria beats regularly at a rate of around 300 beats per minute. The ventricles are protected from this high rate by a refractory AV node. In the ECG, a sawtooth-like regular waveform, also called F waves or flutter waves, appears, see figure 3.28-a. Atrial fibrillation is a faster and more chaotic rhythm than atrial flutter. This kind of arrhythmia is produced by multiple reentry circuits within the atria producing a high rate of atrial contraction between 400 and 700 beats per minute in a chaotic fashion. Fibrillation waves, f waves, are multiform and irregular, see figure 3.28-b.

## 3.5.4 Ventricular Arrhythmia

Reentry mechanisms within the ventricles are responsible for establishing the ventricular arrhythmia which include ventricular tachycardia, ventricular flutter, and ventricular fibrillation.

## 3.5.4.1 Ventricular Tachycardia

Ventricular Tachycardia (VT) defines the case of having in the ECG three consecutive Premature Ventricular Complexes (PVCs) or more. VT is a severe arrhythmia that often impairs heart function considerably and may be a precursor of ventricular fibrillation. The QRS duration of the PVCs in case of VT should be 0.14 sec or greater and the heart rate should be between 100 and 240 beats per minute. VT may be sustained, that is it can last seconds, minutes or hours. It may be also non-sustained when it lasts less than 30 seconds. There are three type of VT that differ in morphology, clinical significance and often in etiology:

1. Monomorphic VT : It is the most frequent type which can be sustained or nonsustained. It is called 'Ventricular flutter' with a rate above 200 beats per minute. The

Figure 3.29. An example of ventricular flutter. Figure is adapted from [75].

<!-- image -->

most current etiology of monomorphic VT is a coronary heart disease (CHD). The prognosis of VT generally depends on the type and severity of the heart disease.

2. Polymorphic VT of type ' Torsade de Pointes' : Torsade de points VT is characterized by a special ECG morphology, where QRS complexes change their polarity around the isoelectric line. This type of VT will usually terminate spontaneously after several seconds or will degenerate into ventricular fibrillation in relatively rare cases. This type of VT will be presented in details later in this chapter.
3. Polymorphic VT without 'Torsade de Pointes' : Polymorphism of QRS complexes without Torsade de Pointes is occasionally seen in patients with severe myocardial damage. Degeneration into ventricular fibrillation is quite common.

## 3.5.4.2 Ventricular Flutter

It is an organized rapid rhythm of the ventricles. QRS complex as well as T wave and P wave can not be seen in the ECG, see figure 3.29. Ventricular flutter can develop into ventricular fibrillation.

## 3.5.4.3 Ventricular Fibrillation

It is much more chaotic rhythm than the ventricular flutter which can lead to cardiac arrest and loss of consciousness, see figure 3.30. The condition can often be reversed by the electric discharge of DC current from a defibrillator.

## 3.5.5 Wolff-Parkinson-White Syndrome

This syndrome is characterized by the presence of an accessory atrioventicular pathway located between the wall of the right or left atria and the ventricles, known as the Bundle of Kent. This pathway allows the impulse to bypass the AV node and activate the ventricles prematurely. Consequently, an initial slur to the QRS complex, known as a delta wave may be observed. The QRS complexes are wide, more than 0.11 sec, indicating that the impulse did not travel through the normal conducting system. The PR is shortened, to less than 0.12 sec, because the delay at the AV node is bypassed. Treatment would involve surgical removal or ablation of one of the pathways [76].

Figure 3.30. An example of ventricular flutter. Figure is adapted from [75].

<!-- image -->

## 3.5.6 Heart Conduction Blocks

A heart conduction block is defined as a blockage of the electrical conduction system of the heart at any level. Blocks that occur within the sinoatrial node (SA node) are described as SA nodal blocks. Blocks that occur within the atrioventricular node (AV node) are described as AV nodal blocks. Blocks that occur below the AV node are known as infra-Hisian blocks [77].

## 3.6 Heartbeat Morphologies

Abnormal heartbeat morphologies can be seen in many arrhythmic cases. Morphological abnormality of the heartbeat can be reflected also by the abnormal structural conditions of the heart, such as ischemia and myocardial infarction as well as atrial and ventricular hypertrophy (mass enlargement) and pericarditis (inflammation of the pericardium). Furthermore, abnormalities in beat morphology can be due to the mutations in ion channels controlling cellular repolarization of the heart, such as Long QT Syndrome, Brugada Syndrome. Other important arrhythmias, which are sometimes linked to mutations in ion channels, are T wave alternans and polymorphic VT type Torsade de 'Pointes', etc...

## 3.6.1 Ischemic Heart Disease

Ischemic Heart Disease (IHD), also known as Coronary Artery Disease (CAD), is a disease characterized by reduced blood supply to the heart. It is usually felt as angina, especially if a large area is affected [78]. Due to the deposition of cholesterol plaques on their walls, the blood vessels will be narrowed or even blocked. This will reduce or stop providing oxygen and nutrients to the myocytes leading to the death of that area of heart tissue and causing

a possible heart attack. Electrocardiography (ECG) may be normal in several patients at rest between the episodes of pain with a possibility for a depression or an elevation of the ST segment and a T wave inversion in several leads. In cases of infarction, there will be ST segment elevation in the ECG, which may gradually evolve. An exercise testing (Treadmill Test-TMT) is often indicated in patients who have symptoms of IHD but have normal ECG patterns [79].

## 3.6.2 Myocardial Infarction

Acute myocardial infarction (AMI or MI), also known as a heart attack, is a serious, sudden heart condition. It causes sometimes loss of consciousness. It occurs when the blood supply to a part of the heart is interrupted, causing death of the local heart tissue. The severity of heart attacks can vary relating to the size the affected area, which disturbs the normal propagation pathways and causes abnormal direction of the electrical impulse. ECG waves of an individual with MI differ significally from the normal ECG waves. There are many morphological varieties of infarction ECG waves depending on the position and size of the infarction in the myocardium.

## 3.6.3 Long QT Syndromes

An abnormally long delay between the depolarization and the repolarization of the heart ventricles is a disease defined as long QT syndrome (LQTS). Specific mutations in ion channels controlling cellular repolarization underlie the various congenital forms of longQT syndrome [80, 81, 82]. Individuals with LQTS have a prolongation of the QT interval in the ECG. The two most common types of LQTS are genetic and drug-induced. Mutations to one of several genes, which are tending to prolong the duration of the ventricular action potential (APD) and lengthening the QT interval, is the cause of genetic LQTS. These LQTS can be inherited in an autosomal dominant or an autosomal recessive fashion. The autosomal recessive forms of LQTS tend to have a more severe phenotype, with some variants having associated syndactyly or congenital neural deafness [83, 84]. A number of specific genes loci have been identified that are associated with LQTS. Because exogenous factors such as antiarrhythmic drugs causing the acquired form of LQTS operate on the same ion channels implicated in congenital LQTS, both forms of the disease may share common electrophysiological mechanisms [85]. Drug induced LQT is usually a result of treatment by anti-arrhythmic drugs such as amiodarone or a number of other drugs that have been reported to cause this problem. Some anti-psychotic drugs, such as Haloperidol and Ziprasidone, have a prolonged QT interval as a rare side effect. Because Long QT syndrom can lead to ventricular arrhythmias, it can cause ventricular fibrillation which is sometimes associated with syncope (loss of consciousness) and sudden cardiac death (SCD) [86, 84].

1. LQT1 : It is the most common type of long QT syndrome, making up about 40 to 55 percent of all cases. The LQT1 gene KCNQ1 has been isolated to chromosome 11p15.5. KCNQ1 codes for the voltage-gated potassium channel KvLQT1 that is highly expressed in the heart. It is believed that the product of the KCNQ1 gene produces an alpha subunit that interacts with other proteins (particularly the minK

beta subunit) to create the IKs ion channel, which is responsible for the delayed potassium rectifier current of the cardiac action potential [84]. Homozygous mutations in KVLQT1 leads to severe prolongation of the QT interval (due to near-complete loss of the IKs ion channel), and is associated with increased risk of ventricular arrhythmias and congenital [87, 84].

2. LQT2 : It is the second most common gene location that is affected in long QT syndrome, making up about 35 to 45 percent of all cases. It involves a mutation of the human ether-a-go-go related gene (HERG) on chromosome 7. The HERG gene (also known as KCNH2) is part of the rapid component of the potassium rectifying current (IKr), That is, the IKr current is mainly responsible for the termination of the cardiac action potential and therefore the length of the QT interval. The normally functioning HERG gene allows protection against early after depolarizations (EADs). Most drugs that cause long QT syndrome do so by blocking the IKr current [87, 84].
3. LQT3 : It involves a mutation of the gene that encodes the alpha subunit of the Na + ion channel. This gene is located on chromosome 3p21-24, and is known as SCN5A (also hH1 and NaV1.5). This mutations slows down the inactivation of the Na + channel, causing prolongation of the Na + influx during depolarization.
4. LQT4 : It involves a mutation in an anchor protein Ankyrin B which anchors the ion channels in the cell. This kind of LQT occurs very rarely.
5. LQT5 &amp; LQT6 : LQT5 involves a mutation in the gene KCNE1 encoding for the potassium channel beta subunit MinK. In the same manner, LQT6 involves a mutation in the gene KCNE2 which encodes for the potassium channel beta subunit MiRP1.
6. LQT7 : It is also called Andersen-Tawil syndrome. It involves a mutation in the gene KCNJ2 encoding for a potassium channel protein Kir 2.1. [88, 84].
7. LQT8 : Also called Timothy's syndrome. It is due to a mutation in the calcium channel Cav1.2 encoded by the gene CACNA1c.

## 3.6.4 Brugada Syndrome

Brugada syndrome is due to a mutation in the gene that encodes for the sodium ion channel in the cell membranes of the myocytes. Gain-of-function mutations in this gene lead to elongation of the cardiac action potential [89, 90]. The pattern seen on the ECG is persistent ST elevations in the electrocardiographic leadsV1-V3 with a right bundle branch block (RBBB) appearance with or without the terminal S waves in the lateral leads that are associated with a typical RBBB. A prolongation of the PR interval is also frequently seen [89, 91]. The cause of death in Brugada syndrome is ventricular fibrillation. The treatment is done via implantation of an implantable cardioverter-defibrillator (ICD) continuously monitoring the heart rhythm and defibrillating an individual if ventricular fibrillation is detected [89, 92].

## 3.6.5 T-Wave Alternans

T-Wave alternans (TWA) is an ECG phenomenon characterized by beat-to-beat alternation or oscillations of the morphology, amplitude, and /or polarity of the T wave, see figure 3.31.

Figure 3.31. An example of T-wave alternans taken from an ECG tape (Pfizer Inc.).

<!-- image -->

TWA is commonly observed in the acquired and congenital and long-QT syndromes (LQTS). Moreover, it is very important prognostic indicator in that it is commonly observed just preceding episodes of Torsade de Pointes [93, 94, 95]. The study in [96] examines the cellular and ionic basis for TWA induced by rapid pacing under condition of mimicking the LQT3 from the congenital LQTS in an arterially perfused canine left ventricular wedge preparation. They recorded transmembrane action potentials from epicardial, M, endocardial cells and 6 to 8 intramural unipolar electrograms simultaneously together with transmural ECG and isometric tension development. A wide spectrum of T-wave and mechanical alternans is produced by increasing the pacing rate from cycle length (CL) of 500 to 400 to 250 ms in presence of sea anemone toxin. Acceleration to CLs of 400 to 300 ms produced mild to moderate beat-to-beat TWA of cells in M region. Acceleration to CLs of 300 to 250 ms caused more pronounced beat-to-beat TWA and APD of the M region, leading to a reversal repolarization sequence across the ventrical wall and thus to alternation in the polarity of T-wave. Torsade de Pointes occurred after an abrupt acceleration of CL associated with marked TWA. In almost all cases, electrical and mechanical alternans were concordant. Both ryanodine and low [Ca 2+ ] completely suppressed alternans of the T wave and shortened APD, suggesting a critical role for intracellular Ca 2+ cycling in the maintenance of TWA. T wave alternans, observed at rapid rates under long-QT conditions, is caused by the alternation of the M-cell action potential duration (APD), leading to exaggeration of transmural dispersion of repolarization during alternate beats, and thus the potential for development of Torsade de Pointes. The pathologic states with TWA are long QT syndrome, myocardial ischemia and infraction, heart failure, sudden infant death syndrome and drug-induced Torsade de Pointes [97]. There is some evidence that TWA is linked to alternations in cellular calcium homeosta-

sis, which significantly influences the action potential duration (APD) [98]. Potassium channels may also play an important role in ischemia-induced TWA. The different sensitivity of KATP channel activation during ischemia between epicardium and endocardium may be linked to TWA at the cellular level [99, 100, 101, 102]. Macroscopic TWA has been reported in patients with the long QT syndrome [94, 103, 104, 96]. Prolongation and unstable state of the ventricular action potential may produce the macroscopic TWA and result in the polymorphic VT known as Torsade de Pointes. The prognostic value of microscopic TWA has not yet been assessed in patients with the long QT syndrome. In patients with the Brugada syndrome, some reports have revealed that intravenous administration of class Ic antiarrhythmic drugs induced macroscopic TWA and resulted in VF [105, 106]. These results suggest that in the Brugada syndrome class Ic antiarrhythmic drugs may accentuate the underlying sodium channel abnormalities, produce an unstable state of repolarization, increase the triggering of PVC, and induce VF. On the other hand, Ikeda et al. [107] reported a low prognostic value of microscopic TWA in patients with the Brugada syndrome. Elevated levels of spatial heterogeneity of repolarization as assessed by second central moment analysis in [108] appear to underlie the progression from elevated TWA levels to more complex patterns and increased risk for VF. Detection of T-wave heterogeneity (TWH) could prove useful in elucidating and clarifying mechanisms of VF. TWH monitored in precordial leads could contribute to stratifying risk for life-threatening arrhythmias, such as Torsade de Pointes.

## 3.7 Torsade de Pointes

The original name of Torsade de Pointes (TDP) comes from French language and means 'twisting of the points', since QRS complexes wing up and down around the isoelectric axis periodically and in a chaotic fashion changing their morphology from beat to beat, see figure 3.32, reminding the original author of the Torsade de Pointes movement in ballet. It is also referred to as torsade or cardiac ballet [93, 94, 95], TDP is a life-threatening arrhythmia closely linked to abnormal cardiac repolarization [109, 110, 111]. The typical initiation of TDP in ECG signal is after, so-called short-long-short (SLS) cycle sequences, see figure 3.32

TDP is associated normally with marked prolongation of QT interval to 600 ms or greater. The etiology and management of torsade are quite different from generic VT cases including polymorphous VT, which are not associated with a prolonged QT interval. Therefore, it is critically important to differentiate between these entities. The delay in phase III of the action potential, which is mediated by the HERG potassium channel, is the underlying basis for the rhythm disturbance. The dysrhythmia is allowed to emerge because of the prolonged period of repolarization and the inhomogeneity of repolarization time among myocardial fibres. Although the precise mechanism of Torsade de Pointes has not been established, recent in vivo studies [112, 113], prefused wedge studies [114, 85, 115], and clinical observations made with monophasic AP recordings [116, 115] have presented evidence in support of the hypothesis that an early afterdepolarization-induced, triggered response initiates Torsade de Pointes but that the arrhythmia is maintained by a re-entrant mechanism. TDP is also characteristic of the congenital long QT syndrome, one form of which is caused by mutations in the HERG gene which encodes the

Figure 3.32. The typical initiation of TDP in ECG signal after short-long-short cycle sequences. The morphology of QRS complexes during its episode is also illustrated.

<!-- image -->

major repolarizating potassium channel Ikr. Furthermore, HERG appears to be the main molecular target for drugs which cause QT prolongation. Cardiac safety is now a major issue in new drug development, because there is increasing awareness that many nonantiarrhythmic drugs can prolong the QT interval and provoke TDP [117]. Moreover, TWA is very important prognostic indicator in that it is commonly observed just preceding episodes of Torsade de Pointes [93, 94, 95]. The mechanisms by which dysfunction at the molecular level translates into functional electrical instability leading to torsade de points (TDP) in LQTS are poorly understood [80]. Previous clinical [94] and experimental [118, 113] observations suggest two hypotheses regarding the electrophysiological basis of TDP. One theory states that TDP arises from triggered activity in competing ventricular foci. Evidence for the triggered activity hypothesis stems from experimental observations [118, 113] and computer models [119] demonstrating an enhanced propensity of cardiac myocytes to generate early after depolarizations (EADs) in response to factors that prolong the action potential duration (APD). Because TDP observed in patients is associated with conditions favoring the development of EADs experimentally, TDP was attributed to EAD-induced triggered activity. This mechanism, however, was challenged because rapid rates accompanying the onset of TDP abruptly shorten repolarization, thereby eradicating the prerequisite condition for EAD-mediated TDP. The second proposed mechanism is based on the association between dispersion of repolarization (DOR) and TDP, suggesting involvement of reentrant excitation. For example, patients with congenital LQTS manifest increased dispersion of QT interval. Moreover, recent observations from surrogate models of LQTS suggest a role for reentrant activity involving relatively large circuits around the cardiac chambers [113, 112]. However, focal (ie, nonreentrant) patterns of activation were also observed in these models, raising addi-

tional uncertainty regarding the underlying cellular mechanisms. Because the Iks current density of the midmyocardial cells (M cells) is relatively weak, they are more sensitive to many APD prolongation conditions than epicardial and endocardial cells [120] and they can play an important role in arrhythmias which are dependent on delayed cardiac repolarization, such as LQTS. Therefore, a transmural optical mapping system was developed to demonstrate a specific role of M cells in generating functional heterogeneities of repolarization that support intramural reentry in LQTS [80]. This system is able to measure electrical heterogeneities between hundreds of cells spanning the ventricular wall, so that a functional topography of M cells as well as their role in promoting transmural DOR and arrhythmias in the presence of cell-to-cell electrotonic interactions can be established. Their data clearly implicate reentry as the mechanism for sustenance of TDP. It has been found that M-cell zones produced discrete refractory borders, which were directly responsible for conduction block and reentry that underlie TDP. It has been exhibited that M cells can express markedly different APDs from neighbouring cells even on multicellular tissues under conditions of normal cell-to-cell coupling, and that M cells are not necessarily distributed uniformly across each transmural layer [80].

Despite relative normalization of the M-cell APD on subsequent beats, reentry persisted as the leading edge of the wavefront propagated into the recovering tail of the circuit. Such dynamic M-cell APD adaptation undoubtedly accounted for the rapidly changing trajectories of the reentrant circuit producing the characteristic polymorphic ECG morphology of TDP. The presence of uniform propagation on the epicardium may explain the appearance of a monomorphic waveform configuration in certain ECG leads but not others. Taken together, these findings suggest the existence of a single rotor during TDP that initially forms in the transmural wall and subsequently meanders into deeper layers of myocardium [80].

Reentrant Mechanism of TDP : The mechanism underlying TDP in this model is shown in a representative example in figure 3.33. After a single premature stimulus (S2), the impulse blocked in the region of most delayed repolarization (Figure A, cells c, d, m1, and m2). The S2 wavefront, however, successfully propagated in the orthodromic direction (along the axon direction) (Figure A, sites a' through e'), circumventing (surrounding) the region of delayed repolarization (Figure A, hatched area). The zone of block of the premature beat (Figure 3.33 A) coincided with the region of most delayed repolarization after the S1 beat (Figure 3.33 R). When the former sites of block (sites c and d) regained excitability, the orthodromic impulse conducted from site e back to site a (Figure 3.33 B), thereby completing the first beat of reentry. A broad area of functional conduction block was present during the initial beats of reentry; however, because of pronounced rate adaptation of M cells [121], these refractory islands rapidly collapsed and were replaced by functional lines of block on subsequent beats (Figures 3.33 C through F). The polymorphic ECG characteristics of TDP were attributable to the fact that lines of block and trajectory of the reentrant circuit varied from beat to beat, initially within the mapped transmural surface and subsequently meandering into deeper myocardial depths. Similar reentrant mechanisms were observed in all experiments.

Figure 3.33. Repolarization map during drive train S1-S1 pacing (R) and depolarization maps during single premature S2 (A) and ensuing TDP caused by transmural reentry (B through F). S2 was applied on the epicardial surface in the wake of the refractory barrier (R) produced by the island of M cells extending from the mid-wall to the epicardial surface. The S2 beat failed to propagate into the region of prolonged refractoriness (cells c, d, m1, and m2), causing block of the antidromic impulse while propagating in a counter clockwise (orthodromic) fashion around the refractory region formed by M cells [80]. Figure is adapted from [80]

<!-- image -->

## Technical Aspects of ECG Recording and Databases Used

## 4.1 The Electrode Skin Interface

There is a basic difference in the generation and representation of electrical signals in biological tissue and metallic conductors. In biological tissue, electrical fields are generated by biochemical processes in which ions are separated, concentrated and moved on account of thermodynamic forces, concentration gradients or impressed electrical potential gradients. From an electrical point of view, biological tissue behaves as an electrolyte. In metallic conductors, electrical current is represented by electron impulses and electron movement [46]. The basic problem in making electrical measurements from biological tissue is therefore that potential differences to be measured reside in an electrolytic medium, while the measurement instruments are connected by metallic wires with electron conduction. The transformation of electron conductivity into ion conductivity takes place by chemical reduction and oxidation reactions:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Metal ions K + go into solution leaving free electrons at the electrode or vice versa. Anions A -carry the electrons through the electrolyte to the respective anodic electrode. The dynamic equilibrium of these reactions follows thermodynamic laws and depends on the metal and electrolyte involved, as well as the temperature of the reaction and concentration of the ions. Separation and concentration of charges at the electrode-electrolyte phase boundary makes this interface itself a generator of electromagnetic fields (EMF).

## 4.1.1 Electrochemical Potentials

A system consisting of a metal electrode immersed in a solution of its own salt is called a half cell. A thermodynamic equilibrium develops between the metal and the salt creating an electrochemical potential which is characteristic of the metal involved. The potential equals the electrical work required to bring a unit charge from infinity to the reference point at the electrode. This is called the electrode potential or half-cell potential. Measurement of this potential requires a second electrode which forms another half cell. This electrode is called a reference electrode, whose potential is arbitrarily set to zero.

## 4.1.2 Reversible and Nonreversible Electrodes

Electrode systems can be subdivided into reversible or nonpolarized and nonreversible or polarized electrodes. Reversible electrodes allow unhindered exchange of charge across the metal-electrolyte interface in both directions, whereas perfectly polarized electrodes exhibit no net charge transfer. To avoid the influence of alternating current on electrode potentials for bioelectric measurements, nonpolarizable reversible electrodes are used.

## 4.1.3 Electrodes of the First and Second Kind

Among the reversible electrodes, there is a distinction between electrodes of the first kind and of the second kind. A metal electrode in contact with a solution of its own ions is called an electrode of the first kind (e.g., silver immersed in a silver nitrate solution). The equilibrium potential of this electrode is a function of the concentration (more correctly of activity) of the cation of the electrode metal in the solution. Electrodes of the first kind often cannot be applied in physiological measurements, since cations of the corresponding electrode material are not present in the physiological preparation or because of the toxicity of the metals. An electrode of the second kind consists of a metal that is in contact with a sparsely soluble salt of its own, where the anion is available in the electrolyte. Typical examples are the Ag | AgCl electrode. The Ag | AgCl electrode is preferably used together with a chloride solution . Since the activity of Cl -anions in biological tissue is relatively high and not related to silver oxidation, caused by current flow, the electrode potential of Ag | AgCl electrodes is rather stable. Therefore, the Ag | AgCl electrode is most suitable for application in routine measurement procedures such as electrocardiography.

## 4.1.4 Polarization or Overvoltages

Since the input impedance of any measurement device is not infinite, a relative small current can flow during measurement. This current shifts the thermodynamic equilibrium and some deviation from the half-cell potential occurs. This deviation is called polarization, or overvoltage.

## 4.1.5 Electrical Properties of the Skin

Anatomically, the skin is a multilayer system composed of the epidermis, the dermis and the subcutaneous layer. The epidermis consists of three sublayers, namely the horny outer layer-stratum corneum, the middle layer-stratum granulosum and the inner layerstratum germinativum. The epidermis is in a process of continuous regeneration. Within the stratum germinativum, cells divide and grow, and during this process are displaced outwards by the newly forming cells underneath them. The cells die off in the stratum granulosum and degenerate further into layers of flat keratinous material which forms the stratum corneum. Dermis and epidermis are interspersed with sweat ducts and hair follicles. The horny layer of dead cells exhibits rather high impedance. Sweating moistens this layer and increases Na + , K + and Cl -concentration. Therefore, skin impedance depends also on the physiological and emotional state of the subject. To obtain highquality ECG records it is desirable to reduce and stabilize the skin impedance as much as

possible. Figure 12.10 shows the factors which influence the skin impedance. Ion migration is very small in the stratum corneum, from which the major part of skin impedance results. The most effective way to reduce skin impedance is to establish a conductive connection between the skin surface and the deeper layers of the skin. This can be achieved by mechanical abrasion of the stratum corneum or by preparation with electrolyte paste. After embrocation of electrolyte paste, water molecules and ions migrate through the horny layer thus forming a conductive bridge between surface and subcutaneous tissue. Since this diffusion takes time, the skin impedance reaches its minimum after 15-20 min.

Figure 4.1. Factors that influence the skin impedance: besides abrasion, increased activity of sweat glands with release of K + , Na + , Cl -and H 2 O increased blood flow reduce the skin impedance. Both effects may be caused by increased physical load or by emotional stress. Figure is adopted and adjusted from [46]

<!-- image -->

However, measurement of the true skin impedance is not possible without involving electrodes which introduce half-cell potentials, electric double layers and resistances of their own. Various side effects must therefore be considered when measurement and interpretation of skin impedance is carried out. Swanson and Webster [122] give an equivalent electrical circuit for the skin impedance consisting of a parallel combination of a capacitor and a leakage resistor which represent the epidermis, and a serial resistor representing the comparatively small resistance of the dermis. The quantities of these elements depend on skin preparation, that is, abrasion, electrolyte paste [123, 124], frequency and density of current flow as well as the physiological state of the skin; and these vary from one individual to another. They also depend on mechanical pressure between electrode and

skin [122] which is of relevance in impedance plethysmography and is sometimes the source of electrode motion artifacts.

## 4.1.6 Electrode Skin Impedance and Offset Voltage

An electrode-electrolyte interface can be equated to a series combination of resistance R and capacitance C , the values of both varying inversely with frequency. A complete electrode-skin interface considering most of the relevant effects has been described with equivalent electric circuits by Gatzke [125] , Geddes [126], and Swanson and Webster [122], whose models are very similar. Therefore the following discussion is based on one of these models, namely in Gatzke [125], see figure 4.2.

Figure 4.2. A complete electrode-skin interface considering most of the relevant effects: part (a), electrical and physical model of the skin-electrode (metal) interface. Part (b): the simplified equivalent electrical circuit. Resistors and a capacitor form a frequency-dependent impedance, which only stabilizes some minutes after electrode application. Figure is adopted and adjusted from [46]

<!-- image -->

In figure 4.2, R b , an ohmic resistor of a few hundred ohms, representing the body fluid. Whereas, the voltage source V s , the capacitance C s and the ohmic resistance R s describes the skin-electrolyte interface.

The voltage V s represents polarization voltages produced by the concentration gradient of ions present in the electrolyte and the body fluid beneath the skin. This potential is a function of electrolyte composition, of its concentration and of skin condition. Resistance R s is inversely proportional to the area of the electrode A , skin condition, skin preparation and electrolyte composition. Moreover, its value decays with increasing time after application. The rate of decay depends on the concentration of the electrolyte. The capacitance C s is a function of skin-electrolyte contact area, electrolyte concentration and skin condition.

The resistance R e describes the ohmic resistance of the electrolyte itself, whose value depends on the concentration of the mobility of the ions and the electrolyte. The voltage V m at the metal-electrolyte interface represents the electrode potential. Its value depends on electrode material and the electrolyte composition. The voltage source V m ( i ) represents polarization voltages which depend strongly on current density and on the material. The resistance R m represents the ohmic resistance between electrode and electrolyte (less then 500 Ω ).The capacitance C m results from the electric double layer formed by the dissociated electrode ions in the solution and the electrode itself.

By taking into account that the frequency range of interest for bioelectric signals covers 0.05-1000 Hz, the equivalent circuit of the electrode model can be simplified as follows: capacitance C m shunts out R m , whereas one equivalent resistor R eq can replace R e and R b resistors. Similarly, if the voltages V m and V m ( i ) are combined to form ´ V m ( i ), the simplified electrode model is depicted in figure 4.2- b.

This model sufficiently describes the effects for all metal electrodes used in electrocardiography, while only the magnitude of relevant parameters varies for different types. An extensive study of the characteristic parameters of routinely used ECG electrodes has been performed by Schmitt and Almasi [127].

## 4.2 Types of Electrodes

Various types of electrodes for recording of bioelectric signals have been developed according to their specific application. In this section, only electrodes used for non-invasive clinical electrocardiography will be discussed. Needle electrodes and microelectrodes used for invasive measurement of intracellular and extracellular electrical activity will not be considered. The need for handy, easy-to-apply electrodes with low offset voltage and low impedance, low artifact pickup, high stability of electrical properties and minimal skin irritation has resulted in the design of a number of different electrode types with varying modes of operation. Some typical examples, and their advantages and disadvantages will be discussed. An extensive description of theory and design of bioelectrodes can be found in [128]. Because of the costs, almost all electrodes for routine recordings are passive. For specific applications, for example, body-surface mapping, buffer amplifiers have been integrated into the electrode housing. Such electrodes are then called active electrodes. Despite the considerable progress in understanding the phenomena at the skin-electrode interface and the progress in electrode technology, this interface is still the weakest link

in the measurement chain. For computerized quantitative ECG analysis, much care has to be taken at this point to obtain high fidelity reproducible ECG signals. In more detail, some typical examples of commonly used ECG electrodes will now be discussed.

## 4.2.1 Plate Electrodes

Figure 4.3 shows typical plate electrodes applied in body-surface electrocardiography. The type illustrated in 4.3-a is used for limb leads, while for chest leads (1-2 cm) the type shown in 4.3-b is used. The large plate electrodes, which were basically introduced in 1917 [129], are made of German silver (an alloy of nickel, copper and zinc), stainless steel, nickel or nickel-plated steel. The metal electrode in this kind of electrode should be separated from the skin by a film of electrolyte paste or by a wet paper in order to obtain a stable offset voltage and low electrode-skin impedance.The smaller chest electrodes are made of nickel, a silver alloy sometimes coated with silver chloride or sintered material containing Ag | AgCl. Plate electrodes are usually fixed by rubber straps. This method is well suited for limb leads, but not for chest leads.

Figure 4.3. Two examples of plate electrodes used in routine electrocardiography: (a) a typical limb-lead electrode which should be applied by using a wet paper between skin and electrode; (b) a typical chest-lead electrode which is applied with electrode gel. Each is held in place by a rubber strap. Figure is adopted and adjusted from [46]

<!-- image -->

## 4.2.2 Suction Electrodes

Figure 4.4 shows two types of suction electrodes (type a and b). The suction-cup electrode (figure 4.4a) can be precisely located and quickly applied and it is well suited for attachment to flat and soft surfaces and tissues. Type (a) is held by a vacuum produced after pressing and releasing the rubber bulb, while type (b), is held by a vacuum produced by an airstream passing through the electrode and using the principle of the Bernoulli pump, (figure 4.4- b). The electrode material of type a is nickel or an alloy. Whereas the electrode in type b can be made of nickel, an alloy or sintered Ag | AgCl. Because of the small contact area, the type-a electrode impedance is high, and because of the close electrode-skin contact, impedance and offset voltage are sensitive to motion. Since the contact area is larger in the type (b) electrode than that of the type (a), skin impedance is smaller. Attachment of type (b) electrodes is much more robust than for suction-cup electrodes and is reliable even on dry or hairy skin. A disadvantage of suction electrodes

is that they can be left on the subject only for a limited period of time in order to avoid serious skin irritation [46].

Figure 4.4. Two examples of suction electrodes: the older model (in (a)) is very frequently used in clinical routine. This type of electrode is often the source of artifacts and poor-quality ECGs since it loses contact and slips during ECG recording. The newer model (in (b)) has two significant advantages: the electrode is reliably held in place, easily attached and detached. The other advantages are a larger electrode area. Figure is adopted and adjusted from [46]

<!-- image -->

## 4.2.3 Fluid-Column Electrodes

Figure 4.5 depicts the principle of fluid-column (floating or liquid junction) electrodes. The electrode elements, which are metal disk and Ag | AgCl sinter element, are recessed so that it does not come in contact with the skin itself. The cavity could be filled with electrode paste which provides the electrolytic bridge between electrode and skin is provided by filling the electrode cavity with electrode paste or by placing an open foam disk placed over the contact area and saturated with electrolyte paste maintaining the distance between the skin and the electrode. In the event of a slight motion of the electrode relative to the body surface, the double layer of charge at the electrode-electrolyte interface is not significantly changed and therefore motion artifacts are minimized. The electrode can be fixed on the skin by a double-sided adhesive tape ring or by a vacuum as shown in figure 4.5.

## 4.2.3.1 Dry Electrodes

The use of electrode paste in routine clinical electrocardiography is a cumbersome procedure. Skin preparation and paste application on each patient for each electrode is time consuming, and multiple-use electrodes have to be cleaned regularly to maintain low noise and low electrode-skin impedance. In long-term applications, paste tends to dry out or may irritate the skin. Efforts have been made to develop pasteless electrodes which could be directly put onto the skin. There are two types of dry electrode: metal-plate electrodes which pick up the ECG in a conductive way; and insulated electrodes, where the metalelectrode surface is coated with a dielectric and the body acts as the other plate of a

Figure 4.5. The principle of fluid-column electrodes : The figure shows an example of an adhesive electrode, where the (Ag | AgCl) electrode element is recessed to provide a gap between electrode housing and skin. The gap is filled with electrolytic gel. The reduction of relative movement and stabilization of pressure between the electrode and skin is achieved by implementing a fluid electrolyte column. Figure is adopted and adjusted from [46]

<!-- image -->

capacitor, so that the signal is picked up capacitively [46]. The problem with both types of electrode is the high input impedance and its instability. The dry metal electrodes, as well as the insulated electrodes, require impedance-transforming amplifiers directly attached to the electrode. So far, the instability and large variation of characteristic electric properties of conductive (impedance, leakage resistance and capacitance) as well as insulated dry electrodes outweigh the advantage of simple attachment of these electrodes.

## 4.2.4 Active Electrodes

Because of the high and unstable impedance of conventional ECG electrodes and because of the existing problem of cable shielding between the electrode and the preamplifier unit, a buffer amplifier should be attached directly to the electrode. Microelectronics now allows the integration of amplifiers into the electrode housing. These electrodes are then called active electrodes.

## 4.3 Electrode Pastes

Electrode jellies and pastes were developed after the introduction of the string galvanometer in order to replace the cumbersome immersion electrodes, which required that the subject be seated with both hands and feet in buckets full of saline solution. Electrode pastes are applied to reduce and stabilize the electrode-skin impedance. Furthermore, the electrochemical equilibrium at the electrode-skin interface develops more quickly when pastes are used. Reduction of electrode-skin impedance is obtained by enrichment with Cl -ions, by moistening the horny layer of the epidermis and by enlargement of the effective contact area. An electrolytic paste layer of 0.1 cm thickness with an area of l cm 2 would result in 0.6-12 Ω , which is negligible compared to the impedance of the epidermis. The following characteristics are desirable for an ideal electrode paste: (a) good reduction of electrode-skin impedance,(b) quick stabilization of the electrical parameters of the electrode-skin interface,(c) simple and quick application,(d) no toxic effects or tendency to irritate the skin, and (e) low costs. Most important is the presence of Cl ions, particularly if Ag | AgCl electrodes are applied [46].

## 4.4 ECG Artifacts and Interference

## 4.4.1 Motivation

Atypical configuration for an ECG acquisition system and the equivalent electrical circuit are shown in figures 4.6 and 4.7 respectively. Via the electrode impedances Z A , Z B and the connecting cables to the ECG amplifier, ECG signal is fed. The displacement current I D arising from electrical fields may flow through the patient to ground, because of stray capacity C D (see figure 4.6). Magnetic fields induce voltages within the connecting cables. A DC offset voltage may be generated at the electrode-skin interface. The magnitude of the offset voltage and interference noise may far exceed that of the ECG signal to be measured. Electrical and mechanical properties of electrodes, cables and ECG amplifiers are usually carefully adjusted to each other. A discussion on interference and noise sources and how to reduce their influence in is presented in this section. The following description is based on papers by [125, 126, 46] and some other works which will be referred accordingly in the text.

Figure 4.6. The typical configuration for ECG acquisition System: the ECG picked up from the body surface may be distorted by internal, muscle tremor for instance, and external noise. Through capacitive coupling to the subject, electric fields from the mains system produce displacement currents . Magnetic fields induce emfs within the lead cables. Figure is adopted and adjusted from [46]

<!-- image -->

The components of the signal at the input of the differential amplifier will now be discussed as a quantitative estimation of noise components:

- V 1 , potential difference appearing at the amplifier input (V)

- V ECG , ECG signal to be measured (V)
- I D , displacement current produced by an alternating electric field ( µA )
- V OFA,B , DC offset voltage at electrodes A , B (V)
- C D , capacitance coupling electric fields to the subject under investigation ( µF )
- f , frequency of the interfering magnetic flux (usually line frequency from mains power (50-60 Hz)
- ˆ B magnitude of the alternating magnetic flux density ( Wbm -2 )
- Z A , Z B , Z G , skin-electrode impedance ( Ω )
- ' · Z IN , amplifier input impedance ( Ω )
- Z I internal body impedance ( Ω )
- K 1 , K 2 , constants
- V D , interference potential from electric fields ( V )
- V CM , common-mode potential ( V )
- V M , interference potential from magnetic fields ( V )
- V AEQ equivalent amplifier noise voltage ( V rms)
- V EM HF or RF electromagnetic interference voltage ( V )

Figure 4.7. The equivalent electric circuit of the typical configuration for ECG acquisition system in figure 4.6: depending on impedance magnitudes and amplifier characteristics, interference effects can be reduced. Figure is adopted and adjusted from [46]

<!-- image -->

For the measurement configuration depicted in Fig. 4.6, the differential voltage obtained at the amplifier input results from the ECG, offset voltages at electrodes A and B , artifact potentials, electric and magnetic interference potentials, a common-mode potential arising from electrode impedance imbalance and amplifier CMRR, electromagnetic HF interference and amplifier noise voltage is as follows:

<!-- formula-not-decoded -->

## 4.4.2 Artifact Potentials

ECG can be heavily distorted by the artifact potentials. Sometimes artifacts closely resemble QRS complexes in shape. Large-amplitude artifacts cannot be eliminated by averaging or filtering. The only way of handling artifact-contaminated data sections is to exclude them from further processing. Artifact potentials have the following sources:

## 4.4.2.1 Myoelectric Activity

It is associated with muscle tremor or other mechanical activity resulting from insufficient relaxation of the patient or from recording in a cold environment, for instance. Myoelectric signals exhibit amplitudes up to 500 µV with a frequency spectrum from 30 Hz up to several kilohertz, thus overlapping the ECG in amplitude and frequency domains. They cannot, therefore, be completely filtered out.

## 4.4.2.2 Skin Artifacts

These kind of artifacts result from changing potential differences between the inner and outer layer of the skin. This potential difference depends on mechanical pressure on the skin. Movement of the patient or of the lead cables do induce also artifacts. Abrading the horny surface layer of epidermis results in reduction of both potential difference across the skin as well as skin impedance. Skin abrading is a very effective method of improving the quality of ECG recording, since the magnitude of the electrode impedance as well as the imbalance between several electrodes can be reduced [46].

## 4.4.2.3 Electrode Motion Artifacts

If the electrode-electrolyte-skin interface is mechanically disturbed, the double layers of charge present may be disrupted. Movement of the electrode produces disturbance of ion distributions, which causes changes in the half-cell potentials. As a result, low-frequency baseline shifts in the ECG record will be pronounced as the segment between P wave offset and QRS complex onset does not lie on the isoelectric line of zero amplitude. Consequently, the isoelectric line of the ECG under study will not be well-defined and the clinical interpretation of the ECG becomes inaccurate and misleading. This wander of the baseline represents a low-frequency component, usually in a range below 0.1 Hz in rest ECG and 0.65 Hz during stress test, within the bandwidth of the ECG. In addition, electrode-motion baseline wander artifact may result from a variety of sources during ECG acquisition presented as follows:

- Coughing or breathing with large chest movement for chest-lead ECGs.
- Poor contact and polarization of electrodes.
- Moving of an arm or a leg in case of limb-lead ECG acquisition.

Furthermore, baseline wander can be caused by the movement of shielded and unshielded ECG cables (it will be presented in details in the following section). Floating electrodes with a liquid bridge between electrode and skin are less sensitive to motion than electrodes with just a thin film of electrolyte paste but mechanical contact to the skin. Motion sensitivity can be further reduced by the application of electrodes with large adhesive mountings which mechanically stabilize the entire region in the vicinity of the electrode [46].

## 4.4.2.4 Cable Motion Artifacts

If an unshielded cable is moved in the presence of an electric field, a displacement current is generated which flows through the electrode impedances Z A or Z B and Z G to ground (figure 4.6). Depending on the velocity of cable movement, the frequency of such an artifact can be expected to lie in the range 0.1-10 Hz; and a baseline disturbance will result as well. Movement of this cable in a static magnetic field, for example the earth's magnetic field, is associated with induction of an electromagnetic field. In addition, movement of shielded cables can produce artifacts. Differential movement between shield, insulator and the central conductor generates displacement currents, since the capacitance between shield and conductor changes [125]. Low cable capacitance and a low dielectric constant of the insulator reduce this effect. Electrostatic fields may also be generated by the ECG technician. Large quantities of synthetic materials with good insulating qualities invite the accumulation of charge in the vicinity of the measurement subject [125]. Movement of the charged material or the subject relative to each other causes a displacement current to flow in the subject. This current returns to earth via the grounding electrode and the associated grounding impedance Z G . (If the patient is not grounded, this current has to flow through the amplifier input resistors Z IN .) Electrostatic artifact voltages may cause large baseline spikes at the amplifier output [46].

## 4.4.3 Electromagnetic Field Interference

Interference is defined as the effect of coupling external electrical energy into the measurement circuit. Normally, it is not caused by galvanic interconnections between external sources and the measurement circuit, but instead either by capacitive coupling with electric fields or inductive coupling with magnetic fields. The most common high-frequency interference, electric as well as magnetic, is from the line frequency (50 Hz or 60 Hz). The later cannot be filtered out without slight distortion of the ECG, since these frequencies lie within the frequency spectrum of ECG signals. Electric fields arise between two points of different electric potential. Electric fields are produced electrostatically or by mainspower wiring, and so on. Magnetic fields are produced by alternating currents and are particularly strong in the neighborhood of mains-power cables with high current density (elevators, transformers, motors, and so on).

## 4.4.3.1 Electric Fields

Interference from electric fields is produced by the mains-power wiring and also by equipment plugged into an outlet but turned off. The AC potentials of the power-supply cable

will still generate an electric field to ground. Coupling of electric fields to the subject from whom an ECG is to be recorded takes place via stray capacity C D of the subject with respect to the environment (see figure 4.6 and 4.7).

The differential voltage V D caused by the displacement current I D , traversing the body impedance Z I in the same direction of the path between electrodes A and B is defined as follows :

<!-- formula-not-decoded -->

where K 1 is a constant, with value between zero and one, including the geometric influences.

## 4.4.3.2 Magnetic Fields

According to Faraday's law, an electromagnetic field (EMF) in any conductive loop, such as that formed by ECG leads A and B is generated by alternating magnetic fields of alternating currents, for example in the mains-power system. The magnitude of this EMF is proportional to the magnitude of the magnetic flux density ˆ B , the frequency f of the magnetic flux (frequency of the field generating AC), the loop area S and a constant K 2 which considers the relative orientation of field and loop in space. The magnitude of magnetically induced interference voltage is obtained from

<!-- formula-not-decoded -->

Since this voltage appears as a differential potential at the amplifier input, the magnetic induction area S should be kept as small as possible by twisting the lead cables and running them close to the body [46].

## 4.4.3.3 Electromagnetic High-Frequency Fields

High-frequency (HF) fields can come from radio and television signals, brush motors, electric switches, other spark generating equipment, electrosurgery and diathermy. Due to the low HF impedance of the coupling capacitance C D , the interference voltages V CM can be very high. Continuous and periodic HF signals are not difficult to deal with as long as amplifiers will not be saturated. However, the HF signal is often modulated with low-frequency components matching the ECG spectrum. These components are fed into the measurement circuit by rectification of the HF signal if there are nonlinearities in the amplifier input circuit. Since these interference components, which are causing spikes in the ECG record, cannot easily be filtered out, the best way to reduce this type of interference is by removal or reduction at source. Bypassing capacitors and HF filters at motors with commutator noise and at the power supply of the electrocardiograph itself often help. Other measures that can be taken include positioning the ECG couch at another place and the use of shielded ECG cables, which should be as short as possible since the HF signal pickup increases with length. If not built in, appropriate HF filters in the input stage of the ECG amplifier should be applied [46].

## 4.5 ECG Amplifiers

ECG amplifiers can be clustered into conventional ECG amplifiers used in various clinical purposes and multi-channel high resolution ECG amplifiers for research applications. The conventional ECG amplifiers are required to drive the write-out system, which may be a paper-strip recorder, an oscilloscope, a magnetic tape unit, a telephone coupling unit or an analog-to-digital converter system for computer processing. Figure 4.8 depicts the basic layout of ECG amplifiers. A buffer amplifier is implemented for transformation of the high and often unbalanced electrode impedance to a low level. The gain of this stage is usually one, but there are systems which use a preamplifier unit between the electrodes and the ECG main amplifier. This stage amplifies the signal by a factor of 5-10.

Figure 4.8. The basic layout of ECG amplifiers. Figure is adopted and adjusted from [46]

<!-- image -->

The network following the buffer amplifier is used to obtain the Wilson central terminal (WCT) for the unipolar chest leads and to derive the Goldberger augmented limb leads. The network is followed by a differential amplifier or an instrumental amplifier. This amplifier stage usually has a gain between 10 and 100. For patient safety, the input part of the amplifier is galvanically separated from the mains power supply by linking via a DC-DC transformer. An RC high-pass filter, coming after the amplifier, removes offset potentials arising from electrodes and other parts of the preceding circuit. The time constant should be not less than 3.2 s to make sure that low frequencies of the ECG signal, particularly of the ST-T segment, are transferred without serious distortion. In some amplifiers, the time constant can be switched to lower values. This removes excessive baseline shift. The succeeding filters assist the removal of line frequency interference and muscle-tremor noise. Actually, they can optionally be switched on or bypassed. However, line frequency interference notch filters in any case distort the ECG, since they also remove components of the QRS complex with the same line frequency.

The final power amplifier provides the necessary current to drive any coupling device as a writing system or an analog-to-digital converter (ADC) system for computer processing.

The gain factor is again of the order of magnitude 10-100 in order to obtain a total gain of the amplifier of approximately 500-1000 which results in 500-1500 mV output voltage . The choice of gain factors for the different stages of the amplifier has to be a compromise between high gain in the preamplifier stage which results in high common-mode rejection and the risk of amplifier saturation by large DC offset voltages. A reasonable compromise, therefore, is to have approximately equal gain factors in the preamplifier and driveramplifier stages. In order to provide further off-line or on-line digital ECG analysis, the signal from the final power amplifier should be fed into an analog-to-digital converter (ADC) and then to a digital signal processor (DSP) unit allowing the implementation for various digital filters and any other sort of on-line processing. The converted digital ECG signals may then be transmitted by various ways to a computer system [46].

## 4.5.1 Differential and Instrumentation Amplifiers

Differential amplifiers are applied for amplification of small biosignals. They allow direct connection of the amplifier input with the measurement points under investigation instead of measuring potentials with reference to ground or to infinity. By the means of differential amplifiers, large noise voltages present at each of the measurement locations can be reduced markedly without filtering, taking into account that the noise is often exceed the biosignal of interest by several orders of magnitude. In principle, a differential amplifier is a composition of two identical single-ended amplifiers with inputs A and B operating in opposition to a common reference, figure 4.9.

Figure 4.9. Differential amplifier schematic. Figure is adopted from [130]

<!-- image -->

Given two inputs V + in and V -in (see figure 4.9), a practical differential amplifier gives an output V out :

<!-- formula-not-decoded -->

where A d is the differential-mode gain and A c is the common-mode gain.

The ability to suppress signals which are common to both inputs is called common-mode rejection (CMR). The CMR ratio (CMRR), measured in positive decibels, is defined by the following equation:

<!-- formula-not-decoded -->

An instrumentation amplifier is a type of differential amplifier that has been specifically designed to have characteristics suitable for use in specific measurements, like biopotential measurements including ECG measurements. These characteristics include very low DC offset, low drift, low noise, very high open-loop gain, very high common-mode rejection ratio, and very high input impedances. They are used where great accuracy and stability of the circuit both short- and long-term are required, [131].

The most commonly used instrumentation amplifier circuit is shown in figure 4.10. The gain of the circuit is

<!-- formula-not-decoded -->

Figure 4.10. Differential amplifier schematic. Figure is adopted from [132]

<!-- image -->

## 4.5.2 Amplifier Specification

## 4.5.2.1 Input Voltage Range and Gain

The voltage to be amplified ranges from micro volts to milli volts. For direct measurement of cellular or myocardial potentials, the input voltage can be expected to lie in a range ± 100 mV . For body-surface ECG measurements, the input voltage reaches ± 10 mV . An

offset voltages of up to several hundred milli volts may arise because of electrode potentials. Thus, the amplifier must be capable of handling such offset voltages.

## 4.5.2.2 Input Impedance

The input impedance is a key figure for the performance of the amplifier. The suppression of interference voltages becomes better as the input impedance becomes larger with respect to electrode impedance. [133] have shown that because of voltage division, the measured amplitudes depend on the ratio of electrode impedance to amplifier input impedance. Recalling figure 4.7, depicting the equivalent circuit diagram, the voltage at the amplifier input V I can be calculated from the source voltage V ECG to be measured as follows:

<!-- formula-not-decoded -->

When ( Z A + Z B ) is zero or is negligible with respect to Z IN , the voltage at the amplifier input V I is equal to the source voltage V ECG .

## 4.5.2.3 Frequency Response

An amplifier can transfer and amplify a signal only within a limited bandwidth, i.e. the difference between the highest and the lowest frequency component to be transferred. The deviation of the magnitude of the transfer function (amplitude response) from unity is also called linear distortion. The range between the lower and upper cutoff frequency of an amplifier is defined as the bandwidth. The transfer function consists of two components: the amplitude response and the phase response. High-fidelity reproduction of a signal also requires an adequate phase response; that is, a linear relationship between frequency and phase angle. Usually this relationship changes at the cutoff frequencies and causes signal distortion. In order to reduce this influence, the bandwidth can be expanded. The figures given here for the bandwidth of ECG amplifiers approximately resemble those given in the AHA recommendations [134]. For the lower cutoff frequency, 0.05 Hz is recommended, and for the upper cutoff frequency, 2500 Hz is advised.

## 4.5.2.4 Common-Mode Voltage Rejection (CMR), Driven-Ground and Driven-Shield Techniques

It was shown that common-mode voltages can be introduced from the mains-power System flowing through the patient via stray capacitances. It may be reduced by grounding the patient, through high amplifier input impedance, by good matching between electrode impedances and by reducing the impedance of the grounding electrode [46]. By feeding back the average part of the common-mode voltage picked up by some electrodes and connecting this inverted signal with the grounding electrode, its impedance will be reduced and the common-mode noise level will be further attenuated. This is called the driven-ground technique , see figure 4.11.

Another way of reducing the effect of the common-mode voltage is called the drivenshield technique . It is done by feeding a non inverted part of the averaged common-mode voltage from several electrodes to the shielding of the lead cables.

Figure 4.11. Increasing the common-mode voltage rejection by the driven-ground technique: Differential amplifier schematic. Figure is adopted from [132]

<!-- image -->

## 4.5.2.5 Amplifier Noise and Drift Stability

Each amplifier, including its passive elements like resistors, capacitors and so on, produces a noise signal, whose level depends on bandwidth. It is called white noise when it is a random signal with a flat power spectral density and has zero autocorrelation, pink noise ( also known as 1 /f noise) when the noise signal shows frequency spectrum such that the power spectral density is proportional to the reciprocal of the frequency or brown/red noise when its spectral density is proportional to 1 /f 2 . Normal ECG amplifiers exhibit a noise level of the order of 1-10 µV with a bandwidth from DC up to 1000 Hz.

The term drift stability refers to constancy of the baseline. A stable baseline is necessary to avoid saturation of the write-out system as well as of any other data storage systems connected.

## 4.6 IBT Multi-Channel ECG Acquisition System

All multi-channel ECG signals used in this work have been measured and recorded with the two multi-channel ECG acquisition systems available in the Institut f¨ ur Biomedizinische Technik (IBT) at Universit¨ at Karlsruhe (TH) by the author. Both system are able to measure up to 64 ECG signals simultaneously. The first one is actually a system of adjusted EEG amplifier(s) employed to record ECG signals from the body torso. The second system, which is better and even newer, is a high resolution biopotential measurement system designed for research applications. More detailed information on both system is presented as follows:

## 4.6.1 The First System ' SynAmps '

This system is called SynAmps , a trade mark of the company NeuroScan [135]. The system is a AC/DC amplifier designed to record a wide variety of multichannel neurophysiological signals up to 32 channels simultaneously. A SynAmps contains the analog components needed to amplify low level neurophysiological signals and the digital components needed to digitize, DC correct, digitally filter, log external events, and transfer data to a host computer. This design allows for high speed acquisition of signals from multiple electrode sites without burdening the host computer which is controlling, displaying, and storing the acquired data. Having two SynAmps systems, we are able at our institute to record up to 64 (32+32) channels simultaneously by connecting both of them and enabling the high performance recording synchronization between them.

## 4.6.1.1 The Electrodes and Cables

Passive disposable dry electrodes with (Ag | AgCl) electrode elements are used with the SynAmps system after performing skin preparation. The electrodes are attached to a set of shielded cables, see figure 4.12, which are assembled by the author to allow higher fidelity and more clinical flexibility for the multi-channel ECG recording than the original EEG cables provided with the systems. The new cables are connected from one side to the electrodes and from the other end to the pre-amplifier box, also called headbox , through one input multi-pin connector provided on the headbox by the manufacture, whereas the original cables can be only connected to their corresponding predetermined locations on the headbox . It has been noticed that the monopolar montage with the original cables is very time consuming and very sensitive to noise. Therefore, the new designed shielded cable set was used in this work.

Figure 4.12. The shielded cables assembled to be used with SynAmps system

<!-- image -->

## 4.6.1.2 The headbox and the Main Unit

The first stage amplification in the DC/AC headbox has a fixed gain factor of 150 and should be placed near to the subject to reduce noise pickup. The amplified signals are

then transferred to the main unit, which has 32 second-stage main amplifiers and 32 successive approximation register (SAR) 16-bit ADC converter with resolution up to 0.007 µV /bit and tracking anti-aliasing filters as well as an analog filter stage for each channel and a digital processing unit, see figure 4.13. Sampling rates are between 100 Hz to 20 kHz. Four high speed digital signal processors (DSPs) are used to control data acquisition and a processor and an electronic flash disk are dedicated to managing the DSPs and communicating with the host computer. Real-time digital filtering performed by the DSPs provides a wide range of filter settings from DC to 10 kHz. A SCSI interface is used to link the SynAmps and computer. All ECG signal recorded by the author using this system is AC coupled and sampled with 1000 Hz and a bandwidth from 0.05 Hz to 400 Hz. CNT is the file format used to save the measured data from the 16-bit-resolution SynAmps . Full specifications and differences of the CNT file formats can be found in [136].

The main drawback of this system was discovered during the first six multi-channel ECG recordings by noticing high degree distortions in the ST segment of ECG beats, see figure 4.14. After investigation, the reason was the 50/60 Hz digital notch filter implemented in the digital processing unit. By disabling the function of this notch filter, relative high level powerline interference, depending on the measurement place, appeared in the ECG recording. Therefore, a simple and effective method was developed to eliminate this 50/60 Hz interference in this regards. This method is presented in detail in section 7.2.1.4.

Figure 4.13. Two SynAmps main units and two headboxes placed on one of the main unit

<!-- image -->

## 4.6.2 The Second System ' ActiveTwo '

This system is called ActiveTwo , which is the newest high resolution, DC amplifier and 24bit resolution biopotential measurement system (including ECG measurements) provided

Figure 4.14. ST segment distortion due to the 50/60 Hz digital notch filter in the SynAmps system

<!-- image -->

by the company BioSemi [131]. With this system, we are able to record up to 64 ECG channels along with a respiration signal simultaneously. Because the ECG main amplifier box, also called the front-end, is battery powered, remarkable elimination of the powerline interference is accomplished.

## 4.6.2.1 ActiveTwo Electrodes

There are indeed a number of practical problems with the current passive electrodes. Unshielded electrode wires are usually the major source of powerline interference [137]. By integrating the first amplifier stage with a sintered Ag | AgCl electrode, ActiveTwo electrodes, which are actually active electrodes, provide at solution for all problems associated with high electrode impedance's and cable shielding. They allow for low-drift DC measurement, extremely low-noise and interference measurements without any skin preparation. All artifacts by cable and connector movements as well as all problems with regards to capacitive coupling between the cable and sources of interference are highly eliminated by these low-output-impedance active electrodes. They have also noise levels as low as the thermal noise level of the electrode impedance [131]. The input impedance of an active electrode is 300 MΩ at 50 Hz

1. Flat-Type Active Electrodes : This electrode consists of the electrode metal, gel cavity and the built-in preamplifier in the electrode housing, figure 4.15. The gel cavity of each electrode is designed to reduce motion artifacts. The electrode has a sintered Ag | AgCl electrode pallet (4mm in diameter), providing very low noise, low offset voltages and very stable DC performance.
2. Both kind of electrodes are attached to the skin by the means of double-sided adhesive tape rings.

Figure 4.15. The Flat-Type Active Electrodes for Multi-channel ECG ActiveTwo System. Figure is adopted from [131]

<!-- image -->

2. Active BSPM Carbon Strips : Flexible rubber strips with integrated carbon electrodes, carbon electrode wire and a preamplifier integrated into the end of the strip is the structure of this kind of electrodes, which are actually designed for BSPM applications, figure 4.16. By choosing different combinations of Panel 4x8 and Panel 4x12 sets, various electrode layouts can be configured.

Figure 4.16. The Active BSPM Carbon Strips for Multi-channel ECG ActiveTwo System. Figure is adopted from [131]

<!-- image -->

## 4.6.2.2 ActiveTwo AD-box

The ActiveTwo AD-box forms an ultra compact, low power galvanically isolated frontend (close to the subject) in which up to 256 sensor-signals are digitized with 24 bit resolution and 31 nV digital resolution, see figure 4.17. One AD-box channel consists of a low noise DC coupled post-amplifier, with a first order anti-aliasing filter, followed by a Delta-Sigma modulator with an oversampling rate of 64, and decimation filter with a steep fifth order Sinc response and high resolution 24-bit output. The digital outputs of all the AD converters (up to 256) are multiplexed and sent to a personal computer via a single optical fiber without any compression or other form of data reduction [131]. There is a chain of three basic noise sources in the ActiveTwo system: the input buffer in the active electrode, the amplifier in the AD-box, and the analog-to-digital converter (ADC), (quantization noise). The dynamic range of ActiveTwo is approximately 110 dB , which means that it has 19 effective bits, and that the 5 least significant bits are noise. Nevertheless, the performance is still impressive since the dynamic range of this 24-bit ADC is a factor of 8 larger than the best 16 bit successive approximation register (SAR) types. All ECG signal recorded by the author using ActiveTwo system is sampled with 2

Figure 4.17. Multi-channel ECG ActiveTwo AD-box with battery. Figure is adopted from [131]

<!-- image -->

kHz, which gives 400 Hz bandwidth since the analog bandwidth of this system is always 1 / 5 th of the sample rate.

The BioSemi Data Format (BDF) is the file format used to save the measured data from the 24-bit-resolution ActiveTwo . BDF is a 24 bit version of the popular 16 bit European Data Format. Full specifications and differences of the BDF/EDF file formats can be found [136].

Furthermore, a full description on the specifications for the biopotential measurement system, type ActiveTwo with two-wire active electrodes, can be found in [138].

## 4.6.2.3 The Respiration Belt

The ActiveTwo system used in our institute is able to record the respiration signal simultaneously along with the 64-channel ECG signal. The respiration signal is obtained by using a respiration belt directly plugged into the ActiveTwo AD-box.

## 4.7 IBT Multi-Channel ECG Lead System

The conventional 12-lead ECG and VCG techniques were developed from empirical considerations and from the representation of the electrical activity of the heart as a simple dipole. In contrast, the objective of electrocardiographic body-surface potential mapping is to measure 'all' available ECG Information, which requires extensive spatial sampling. Multi-channel ECG lead systems have been characterized as 'complete' or 'limited'. The former implying the actual sampling of 'all' data (most of the thoracic surface) and the latter implying the sampling of a small number of sites for approximating and optimizing complete distributions to a pre-specified level of accuracy [46].

There have never been standards for lead systems since mapping has been relegated primarily to research laboratories. Using recordings with 'complete' leads (about 200), estimates can be made of the minimum number of leads that is needed to obtain the same accuracy [47]. Zywietz determined this to be approximately 33 by applying the

spatial sampling theorem to data sets of 209 leads [139]. A two 32-lead (limited-lead) recording array was designed on the basis of initially recorded complete 192-lead data on 132 subjects by Lux et al. [140, 51]. In their complete lead, electrodes were evenly spaced in 16 vertical columns of 12 recording sites with the latter also being equally spaced between the sternal notch and the umbilicus. The first 32-limited-lead set, known as the Lux limited has 6 electrodes on the back (see figure 4.18), whereas the second set, known as Lux anterior does not have any posterior electrode sites (see figure 4.19).

Lux limited is basically used to develop a 64-channel ECG lead system in our institute, called IBT Multi-Channel ECG Lead System , because it is expected from this set to provide about the same information as 192 equally distributed leads (complete lead system) with some posterior electrodes on the back.

32 electrodes were added to Lux limited in order to provide IBT Multi-Channel ECG Lead System . These additional electrodes are shown in figure 4.20, whereas the labels of all electrodes in IBT Multi-Channel ECG Lead System are illustrated in figure 4.21. The electrodes added allow the following:

1. ability to derive the bipolar and the augmented unipolar limb leads using the electrodes A13, C13 and C24 shown in the figure 4.21 and referring to Mason and Likar Lead System explained in section 3.3.1.4.
2. ability to derive the unipolar precordial leads using the electrodes A7, B5, B18, C6, C18 and A2 shown in the figure 4.21.
3. more compatibility and effectivity to place the Active BSPM Carbon Strips of the ActiveTwo system very fast with minimal error as illustrated in figure 4.21, where four Active BSPM Carbon Strips with twelve electrodes each can cover completely the left anterior part of the torso.

The reference and the ground electrode, denoted as RF and GN (right-leg electrode) respectively in the figure 4.21 , are placed in the region of the right iliac fossa as mentioned in Mason and Likar Lead System explained in section 3.3.1.4.

## 4.8 ECG Databases

In this section, a complete description about all ECG databases used in this work is given. These databases can be differentiated between multi-channel ECG databases, annotated ECG databases and ECG databases recorded during some pharmaceutical studies.

## 4.8.1 Multi-Channel ECG Databases

As mentioned before, all multi-channel ECG signals used in this work have been measured and recorded with the already-presented two IBT Multi-channel ECG acquisition systems by the author. All measurements, done with ActiveTwo system, were recorded with respiration signal.

## 4.8.1.1 64-Channel ECG Databases from the SynAmps System

Since the powerline interference of the first system, the SynAmps system, is relatively high, efforts were made to develop a suitable method to filter this noise out. Therefore,

Figure 4.18. The 32-lead Lux limited recording array estimating the complete 192-lead data on 132 subjects by Lux et al with 6 electrodes on the back

<!-- image -->

the 64-channel ECG signals measured by this system were used only to develop that method and were not used as input to any other method in this work avoiding any additional possible error. In details, four 64-channel ECG signals were recorded from young volunteers, who did not suffer from any cardiac problems (see figure 4.22 as an example). A screen-shot during one of these ECG recordings is illustrated in the figure 4.23.

## 4.8.1.2 64-Channel ECG Databases from ActiveTwo system

64-channel ECG measurement along with one channel respiration signal recording were done on five young volunteers, who also did not suffer from any cardiac problems. The quality of these recorded ECG signals were remarkably better than the ECG recorded by SynAmps system (see figure 4.22 as an example). The duration of these signals varies between one and five minutes. A screen-shot during one of these ECG recordings is illustrated in the figure 4.25.

## 4.8.2 Annotated ECG Databases

Several different standard databases are stored at Physionet.org, which are recorded and analysed to allow comparison between different ECG signal processing approaches,

Figure 4.19. The 32-lead Lux anterior recording array estimating the complete 192-lead data on 132 subjects by Lux et al without any electrodes on the back

<!-- image -->

namely automatic ECG segmentation algorithms. One of these database is the MIT/BIH arrhythmia database, which has been used in this thesis. The MIT/BIH arrhythmia database contains 48 half-hour excerpts of two-channel ambulatory ECG recordings, obtained from 47 subjects studied by the Boston's Beth Israel Hospital (BIH) Arrhythmia Laboratory between 1975 and 1979. Twenty-three recordings (records number Ixx) were chosen at random from a set of 4000 24-hour ambulatory ECG recordings collected from a mixed population of inpatients (about 60%) and outpatients (about 40%) at the BIH. The remaining 25 recordings (records number 200 and above) were selected from the same set to include less common but clinically significant arrhythmias that would not be well-represented in a small random sample. The recordings were digitized at 360 samples per second with 11-bit resolution over a 10 mV range. Two or more cardiologists independently annotated each record. Disagreements were resolved to obtain the computerreadable reference annotations for each beat included with the database, namely the location R peaks. Altogether there are over 100000 QRS-complexes in this database. While some records contain clear QRS-complexes and few artifacts (e.g., records 100-107), for some records the detection of QRS complexes is very difficult due to abnormal shapes, noise, and artifacts (e.g., records 108 and 207) [141, 142].

Figure 4.20. The IBT 64-Channel ECG Lead System based on Lux limited

<!-- image -->

## 4.8.3 Clinical-Trials ECG Databases

60 normal and 10 Torsade-de-Pointes two-channel tapes from different studies recorded during Dofetilide clinical trials (Pfizer, Inc.) are used in this Thesis. All tapes are 24hour ambulatory Holter recordings. All Torsade-de-Pointes tapes have non-sustained TDP episodes. Atrial Fibrillation (AF) is reported in eight Torsade-de-Pointes tapes.

Figure 4.21. The IBT 64-Channel ECG Lead positions on the human torso with the corresponding electrode labels

<!-- image -->

Figure 4.22. The IBT Multi-Channel ECG electrode set applied on a young volunteer during one measurement with the SynAmps system

<!-- image -->

Figure 4.23. A screen-shot during one of the IBT 64-Channel ECG recordings with the SynAmps system: it is important to note that the signal appearing on the screen is digitally notch-filtered, whereas the recorded signal is not passed to any powerline interference notch filter

<!-- image -->

Figure 4.24. The IBT Multi-Channel ECG electrode set and the respiration belt attached to a young volunteer during one measurement with the ActiveTwo system

<!-- image -->

Figure 4.25. A screen-shot during one of the IBT 64-Channel ECG recordings with the ActiveTwo system and the acquisition program provided by the manufacture

<!-- image -->

## Applied Methods and Mathematics

## 5.1 Mathematical Basics

## 5.1.1 Expected Value

The Expected Value, also called mathematical expectation or ensemble average, of a function f ( x ) in a single continuous variable x is denoted as E [ f ( x )] or 〈 f ( x ) 〉 and given by the first-order moment of its probability density function (PDF) as follows:

<!-- formula-not-decoded -->

where P ( x ) is the probability function. For a single discrete variable, it is defined by

<!-- formula-not-decoded -->

When the PDFs of the random processes of concern are not know and when dealing with random processes that are observed as function of time or stochastic processes, like biosignals, it is common to approximate the statistical expectation operation by averages computed using a collection or ensemble average at every point of time. Suppose we have M observations of the random process x ( n ) as function of time. We may estimate the mean of the process at a particular instant of time n 1 as:

<!-- formula-not-decoded -->

and then we obtain an averaged function of time x , also called mean value, as

<!-- formula-not-decoded -->

## 5.1.2 Variance and Covariance

The variance function contains for each sample the ensemble average of the squared deviation from the mean value for that sample. The variance function V ar x is given by

<!-- formula-not-decoded -->

where σ x ( n ) is the standard deviation, also denoted as SD , and M is the number of observations of the variable x . The covariance function, also called autocovariance function, describes the average joint deviation from the mean value for two samples n 1 and n 2 is defined by

<!-- formula-not-decoded -->

A positive covariance value indicates that the deviations from the mean value for these two samples, in average, have the same sign, while a negative value indicates that the deviations tend to have opposite sign. The covariance matrix C x is defined in vector form as follows:

<!-- formula-not-decoded -->

which is symmetric. Suppose a training set with N samples and each sample can be expressed by a row vector with the size of L , S i = [ S i 1 , S i 2 , · · · , S iL ] , then the average vector S of the training set S and the covariance matrix C s can be computed as follow:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## 5.1.3 Correlation

Mathematically, the correlation function r x for a random stochastic process x ( n ) is defined by

<!-- formula-not-decoded -->

Although the correlation function does not reflect deviations from the mean value, its interpretation is similar to that of the covariance function. The correlation matrix is defined by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Because a close relation exists between the correlation and covariance matrices, a zeromean process will have identical covariance and correlation matrices.

<!-- formula-not-decoded -->

In probability theory and statistics, correlation, also called Pearson product-moment correlation coefficient , indicates the strength and direction of a linear relationship between two different random variables or stochastic processes, x ( n ) and y ( n ) for instance.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The corresponding correlation matrix is defined by

<!-- formula-not-decoded -->

## 5.2 Principal Component Analysis (PCA)

PCA is a linear transformation that transforms the data to a new coordinate system such that the greatest variance by any projection of the data comes to lie on the first coordinate (called the first principal component), the second greatest variance on the second coordinate, and so on. PCA can be used for dimensionality reduction in a dataset while retaining those characteristics of the dataset that contribute most to its variance, by keeping lower-order principal components and ignoring higher-order ones. Such loworder components often contain the 'most important' aspects of the data, but this is not necessarily the case, depending on the application. PCA is also called the (discrete) Karhunen-Lo` eve transform (or KLT, named after Kari Karhunen and Michel Lo` eve) or the Hotelling transform (in honor of Harold Hotelling). PCA has the distinction of being the optimal linear transformation for keeping the subspace that has largest variance. This advantage, however, comes at the price of greater computational requirement if compared, for example, to the discrete cosine transform. Unlike other linear transforms, the PCA does not have a fixed set of basis vectors. Its basis vectors depend on the data set [143].

## 5.2.1 Orthogonal and Orthonormal Series Expansions

A biosignal x i can be composed of useful noise-free signal s i and pure noise signal v i :

<!-- formula-not-decoded -->

On the other hand, x i can be represented by a linear combination, or so-called series expansion, of basics functions ϕ k .

where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The coefficient vector w i , also called weighting vector, is the representation of x i in terms of the basis ϕ 1 , ϕ 2 , . . . , ϕ N . If the basis functions are mutually orthogonal, the representation of x i in 5.2.1 will be called an orthogonal series expansion and if they are orthonormal, i.e. orthogonal and their energy normalized to one, the representation will be called then an orthonormal series expansion [33]. In case of orthonormality we will have the following:

<!-- formula-not-decoded -->

/negationslash

Thus, each weight w i,k results from a correlation operation, or inner product, between x i and the basis function

<!-- formula-not-decoded -->

## 5.2.2 Truncated Orthonormal Series Expansions

Since the orthonormal series expansion in 5.18 represent the sum of the useful signal s i and the noise as well v i , it is very necessary to apply a good separation between both signal components in order to get an acceptable estimation for the useful signal. In other words, we need to find a subset of basis functions that can provide an adequate representation of the useful part of the original signal s i . This can be done through a truncated series expansion [33]. One possibility to achieve this goal is to decompose the matrix Φ into two matrices, Φ s and Φ v whose columns represent the signal and the noise parts, respectively,

<!-- formula-not-decoded -->

where the size of Φ s is N × K and of Φ v is N × ( N -K ); K is a natural number which is smaller than N and denotes the number of the basis function that approximate the signal s i with minimum error. Depending on the equation 5.20 we can write x i as follows:

<!-- formula-not-decoded -->

The left-hand side sum in the equation 5.21 represents the best approximation for the noise-free signal ̂ s , whereas the right-hand side sum represents the best approximation for the noise ̂ v providing that the best K is taken with the smallest level of approximation error. The space χ is defined by the set of all vectors which can be represented by linear combinations of the basis { ϕ 1 , ϕ 2 , . . . , ϕ N } , denoted

<!-- formula-not-decoded -->

In terms of vector spaces, truncation may be related to what is called decomposition of the space χ into χ s and χ v as follows,

<!-- formula-not-decoded -->

where

<!-- formula-not-decoded -->

and ⊕ denotes the direct sum of the two subspaces.

## 5.2.3 Karhunen-Lo` eve Expansion

The Karhunen-Lo` eve expansion is actually the best and optimal truncated orthonormal series expansion compared to any other. Karhunen-Lo` eve method implies the mean-square error (MSE) to minimize the error in estimating the noise signal ̂ v in the following equation:

The aim is to find the set of ϕ k 's that makes ̂ s resemble s as closely as possible. This can be done by minimizing the noise power ε estimate in the MSE sense,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

̂ ̂ By assuming that the signal and the noise are uncorrelated and that the noise is white, the error ε can be written as

<!-- formula-not-decoded -->

where R x is the correlation matrix characterizing the ensemble of original signals x . In order to solve the minimizing problem, a Lagrange multiplier technique will be used and the new function L to be minimized is defined by

<!-- formula-not-decoded -->

where λ k 's are Lagrange multipliers related to each of the constraints. By taking the gradient of L with respect to Φ k and setting the result to zero ∇ Φ k L = 0, we will yield

<!-- formula-not-decoded -->

By inserting 5.28 into 5.26 the final MSE will be expressed as

<!-- formula-not-decoded -->

and thus ε is minimized when the N -K smallest Lagrange multipliers are chosen. The equation 5.29 establishes the very important finding that the basis functions Φ k should be chosen as the eigenvectors of the correlation matrix R x and that Lagrange multipliers λ k are in fact the corresponding eigenvalues.

λ k are positive- or zero-valued and they are arranged in decreasing order

<!-- formula-not-decoded -->

The equation in 5.28 can be expressed in a compact matrix form as follows:

<!-- formula-not-decoded -->

where Λ is a diagonal matrix whose diagonal elements are equal to the eigenvalues λ 1 , λ 2 , . . . , λ N . Since Φ is orthogonal, R x can be expressed as follows:

<!-- formula-not-decoded -->

The average energy associated with each coefficient W after using the equation 5.18 and 5.32 is denoted as because the coefficients of W are mutually uncorrelated,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

/negationslash

the average energy associated with each coefficient w k will thus be equal to λ k [33]. Furthermore, in energy terms, a performance index R K can be defined to reflect how well the truncated series expansion approximates the ensemble:

<!-- formula-not-decoded -->

In the case when x is the zero-mean signal of the signal y for example

<!-- formula-not-decoded -->

the correlation matrix R x of the zero-centered signal x will be in fact the covariance matrix C y of the signal y as follows:

<!-- formula-not-decoded -->

## 5.2.4 Methods to Calculate PCA

## 5.2.4.1 The Covariance Matrix Method

The goal is to transform a given data set X of dimension M to an alternative data set Y of smaller dimension L . Equivalently, we are seeking to find the matrix Y , where Y is the Karhunen-Lo` eve transform (KLT) of matrix X :

<!-- formula-not-decoded -->

1. Organizing the data set : Suppose a training set X with N samples and each sample X i can be expressed by a row vector with the size of M as follows:

<!-- formula-not-decoded -->

The training set is placed into a single matrix X of dimensions N × M , so that N are the number of observations and M is the dimension of the observation vector.

<!-- formula-not-decoded -->

2. Calculate the empirical mean raw vector : The empirical mean along each dimension m = 1... M is calculated. Afterward, all computed mean values are placed into an empirical mean row vector u of dimension M .

<!-- formula-not-decoded -->

3. Calculate the deviations from the mean : The empirical mean row vector u is subtracted from each row of the data matrix X . Then a new mean-subtracted data matrix B ( N × M ) is derived.

<!-- formula-not-decoded -->

where h is a column vector of ones and size of N x1 :

<!-- formula-not-decoded -->

4. Find the covariance matrix : As illustrated before, the M × M empirical covariance matrix C is calculated from the outer product of the zero-centered matrix B with itself:

<!-- formula-not-decoded -->

where E is the expected value operator, ⊗ is the outer product operator, and ∗ is the conjugate transpose operator.

5. Find the eigenvectors and eigenvalues of the covariance matrix : This step will typically require the use of a computer-based algorithm for computing the eigenvalue matrix D and the eigenvector matrix V of the covariance matrix C :

<!-- formula-not-decoded -->

The matrix D will take the form of an M × M diagonal matrix, where D [ p, q ] = λ m for p = q = m is the m th eigenvalue of the covariance matrix C , and D [ p, q ] = 0 for p = q.

/negationslash

The matrix V , also of dimension M × M , contains M column vectors, each of length M , which represent the M eigenvectors of the covariance matrix C .

The eigenvalues and eigenvectors are ordered and paired. The m th eigenvalue corresponds to the m th eigenvector.

6. Rearrange the eigenvectors and eigenvalues : The columns of the eigenvector matrix V and eigenvalue matrix D are sorted out in order of decreasing eigenvalues thereby maintaining the correct pairings between the columns in each matrix.
7. Compute the cumulative energy content for each eigenvector : The eigenvalues represent the distribution of the source data's energy among each of the eigenvectors, where the eigenvectors form a basis for the data. The cumulative energy content g for the m th eigenvector is the sum of the energy content across all of the eigenvectors from 1 through m :

<!-- formula-not-decoded -->

8. Select a subset of the eigenvectors as basis vectors : Save the first L columns of V as the M × L matrix W :

<!-- formula-not-decoded -->

where 1 ≤ L ≤ M . The vector g is used as a guide in choosing an appropriate value for L . The goal is to choose as small a value of L as possible while achieving a reasonably high value of g on a percentage basis. For example, one may want to choose L so that the cumulative energy g is above a certain threshold, like 95 percent. In this case, choose the smallest value of L such that

<!-- formula-not-decoded -->

9. Compute PCA scores : The projected PCA-scores or the reconstruction parameter vectors (RPV) are the columns of the matrix Z ( N × M ), namely Z i 1 , Z i 2 and Z iM , where i = 1 ...N . The matrix Z is calculated by multiplying the eigenvector matrix with the zero-mean data matrix from the left as follows:

<!-- formula-not-decoded -->

The rows of Z correspond to the observations, whereas the columns refer to the components or dimensions.

In fact, the projected PCA-scores or vectors represent the Karhunen-Lo` eve transform (KLT) of the data vectors in the columns of matrix X , equation 5.48.

## 5.2.4.2 The Singular Value Decomposition (SVD)

SVD does not employ any covariance or correlation matrix in its calculation. The goal of SVD is also to transform a given data set X of dimension M to an alternative data set Y of smaller dimension L as follows:

<!-- formula-not-decoded -->

1. Organizing the data set : Suppose a training set with N samples and each sample X i can be expressed by a row vector with the size of M as follows:

<!-- formula-not-decoded -->

The training set is placed into a single matrix X of dimensions N × M , so that N are the observations and M are the dimensions.

<!-- formula-not-decoded -->

2. Calculate the empirical mean raw vector : The empirical mean along each dimension m = 1... M is calculated. Afterward, all computed mean values are placed into an empirical mean row vector u of dimensions M .

<!-- formula-not-decoded -->

3. Calculate the deviations from the mean : The empirical mean row vector u is subtracted from each row of the data matrix X . Then a new mean-subtracted data matrix B ( N × M ) is derived.

<!-- formula-not-decoded -->

where h is a column vector of ones and size of N x1 :

<!-- formula-not-decoded -->

4. Find the matrix A : The matrix A has the size of M × N and is calculated as follows:

<!-- formula-not-decoded -->

5. Apply Singular Value Decomposition on the matrix A : SVD performs a factorization on the matrix A of the following form:

<!-- formula-not-decoded -->

where U is an N × M unitary matrix, the matrix Σ is of size M × M with nonnegative numbers on the diagonal and zeros off the diagonal, and V ∗ denotes the conjugate transpose of V . In fact, The matrix V contains a set of orthonormal input or analysing basis vector directions for A . In other words, the matrix V is equal to the matrix V in the section 5.2.4.1 on page 75. It contains also M column vectors, each of length M , which represent exactly the M eigenvectors of the covariance matrix C . The matrix Σ contains the singular values, which can be thought of as scalar gain controls by which each corresponding input is multiplied to give a corresponding output. The matrix U contains a set of orthonormal output basis vector directions for A . The diagonal eigenvector matrix D of the covariance matrix C in the section 5.2.4.1 can be derived here by applying an array multiplication (element-by-element product) of the diagonal matrix Σ with itself as follows:

<!-- formula-not-decoded -->

Afterward, the steps 6 through 9 in the section 5.2.4.1 are applied exactly in the same manner on the matrices V and D in this section. Similar results are finally obtained from both methods, i.e. the covariance matrix and SVD methods.

## 5.2.4.3 The Correlation Matrix Method

The big drawback of PCA based on covariance matrices is the sensitivity of the principal components (PCs) to the units of measurement used in the data matrix X . If there are large differences between the variances of the elements of X , then those variables whose variances are largest will tend to dominate the first few PCs. Therefore, a major argument for using correlation, rather than covariance, matrices to define principal components is that the results of analysis for different sets of random variables are more directly comparable than for analysis based on covariance matrices.

If all the elements of X are measured in the same units, like the work in this thesis, the covariance matrix method will be entirely appropriate. This method is applied on the data set by calculating the eigenvectors and the corresponding eigenvalues of the correlation matrix derived from the original data or of the covariance matrix of the standardized data matrix from the original data matrix. The standardized data matrix is denoted as X sta and defined as follows:

where

<!-- formula-not-decoded -->

and u is the empirical mean of the original data matrix X as defined in 5.42.

<!-- formula-not-decoded -->

## 5.2.5 Hotelling's T Squared Statistics

Hotelling's T-square statistic, T 2 , is defined as follows:

<!-- formula-not-decoded -->

where N is the number of observations, M is the number of the dimension of the matrix X , defined in 5.39 and in 5.40. z ik is the PCA score corresponding to the i th observation and the k th dimension of the matrix Z defined in 5.48.

<!-- formula-not-decoded -->

The matrix Z contains the PCA scores , also called the reconstruction parameter vectors . λ k ∈ D is the k th eigenvalue of the covariance C derived from the zero-centred data matrix of the original data matrix X .

T 2 is also defined as the squared Mahalanobis distance, D 2 i ,

<!-- formula-not-decoded -->

From equation 5.45, C and C -1 can be re-written as follows:

<!-- formula-not-decoded -->

And from equation 5.48, ( X i -X ) and ( X i -X ) T can be re-calculated as follows:

<!-- formula-not-decoded -->

Using the equations 5.63 and 5.64 in 5.65, T 2 will be derived as,

<!-- formula-not-decoded -->

Hotelling's T squared is defined as an overall measure of variability in a dataset. It is actually a quantity indicating the overall conformance of an individual observation vector to its mean or an established standard [144]. In other words, Hotelling's T 2 is a measure of the multivariate distance of each observation from the center of the data set [1]. Because the use of PCA and Hotelling's T squared shows high efficiency, they are applied extensively in Statistical Process Control (SPC), finding outliers and measures of quality control [145].

## 5.3 Finite &amp; Infinite Impulse Response Filters

## 5.3.1 Z-Transform

In mathematics and signal processing, the Z-transform converts a discrete time domain signal, which is a sequence of real numbers, into a complex frequency domain representation. The Z-transform, like many other integral transforms, can be defined as either a one-sided or two-sided transform.

- Bilateral Z-Transform : The bilateral or two-sided Z-transform of a discrete-time signal x [ n ] is the function X ( z ) defined as:

<!-- formula-not-decoded -->

where n is an integer and z is, in general, a complex number:

<!-- formula-not-decoded -->

where A is the magnitude of z , and φ is the angular frequency (in radians per sample).

- Unilateral Z-Transform : Alternatively, in cases where x [ n ] is defined only for n ≥ 0, the single-sided or unilateral Z-transform is defined as

<!-- formula-not-decoded -->

In signal processing, this definition is used when the signal is the output of a causal system with output and internal states that depend only on the current and previous input values.

## 5.3.2 Laplace Transform

The Laplace transform of a function f ( t ), defined for all real numbers t ≥ 0, is the function F ( s ), defined by:

<!-- formula-not-decoded -->

The parameter s is in general complex:

<!-- formula-not-decoded -->

This integral transform has a number of properties that make it useful for analysing linear dynamical systems. The most significant advantage is that differentiation and integration become multiplication and division, respectively, with s . (This is similar to the way that logarithms change an operation of multiplication of numbers to addition of their logarithms.) This changes integral equations and differential equations to polynomial equations, which are much easier to solve.

The Laplace transform can be alternatively defined as the bilateral Laplace transform or two-sided Laplace transform by extending the limits of integration to be the entire real axis. If that is done the common unilateral transform simply becomes a special case of the bilateral transform where the definition of the function being transformed is multiplied by the Heaviside step function. The bilateral Laplace transform is defined as follows:

<!-- formula-not-decoded -->

The Z-transform is simply the Laplace transform of an ideally sampled signal with the substitution of where T = 1 /f s is the sampling period (in units of time e.g. seconds) and f s is the sampling rate in Hertz.

<!-- formula-not-decoded -->

## 5.3.3 LTI System Theory

LTI system theory investigates the response of a linear system, time-invariant system to an arbitrary input signal. The defining properties of any linear time-invariant system are, of course, linearity and time invariance:

- Linearity means that the relationship between the input and the output of the system satisfies the scaling and superposition properties. Formally, a linear system is a system which exhibits the following property: if the input of the system is

<!-- formula-not-decoded -->

then the output of the system will be

<!-- formula-not-decoded -->

for any constants A and B, where y i ( t ) is the output when the input is x i ( t ).

- Time invariance means that whether we apply an input to the system now or T seconds from now, the output will be identical, except for a time delay of the T seconds. More specifically, an input affected by a time delay should effect a corresponding time delay in the output, hence time-invariant.

The fundamental result in LTI system theory is that any LTI system can be characterized entirely by a single function called the system's impulse response. The output of the system is simply the convolution of the input to the system with the system's impulse response. This method of analysis is often called the time domain point-of-view. The same result is true in case of discrete-time linear shift-invariant systems, in which signals are discrete-time samples, and convolution is defined on sequences. Equivalently, any LTI system can be characterized in the frequency domain by the system's transfer function, which is the Laplace transform of the system's impulse response (or Z transform in the case of discrete-time systems). As a result of the properties of these transforms, the output of the system in the frequency domain is the product of the transfer function and the transform of the input. In other words, convolution in the time domain is equivalent to multiplication in the frequency domain.

## 5.3.4 Finite Impulse Response Filter (FIR)

A finite impulse response (FIR) filter is a type of digital filter. It is 'finite' because its response to a Kronecker delta impulse ultimately settles to zero. This is in contrast to infinite impulse response filters which have internal feedback and may continue to respond indefinitely.

The difference equation defining how the input signal is related to the output signal of an FIR filter is as follows:

<!-- formula-not-decoded -->

where P is the filter order, x ( n ) is the input signal, y ( n ) is the output signal and b i are the filter coefficients. The previous equation can also be expressed as

<!-- formula-not-decoded -->

To find the impulse response we set x ( n ) = δ ( n ) where δ ( n ) is the Kronecker delta impulse. The impulse response for an FIR filter follows as

<!-- formula-not-decoded -->

The Z-transform of the impulse response yields the transfer function of the FIR filter

<!-- formula-not-decoded -->

We note that Z { δ ( n ) } = 1 then with the definition of the impulse response and the time shift property of the Z-transform follows

<!-- formula-not-decoded -->

The transfer function allows us to judge whether or not a system is bounded-input, bounded-output stability (BIBO) stable. To be specific the BIBO stability criterion requires all poles of the transfer function to have an absolute value smaller than one. In other words all poles must be located within a unit circle in the z -plane . To find the poles of the transfer function we have to extend it with z P z P and arrive at

<!-- formula-not-decoded -->

The FIR transfer function contains P poles for z = 0. Since all poles are at the origin, all zeros are located within the unit circle of the z -plane ; therefore all FIR filters are stable.

## 5.3.5 Infinite Impulse Response Filter (IIR)

IIR (infinite impulse response) is a property of signal processing systems. Systems with that property are known as IIR systems or if we are dealing with electronic filter systems IIR filters. They have an impulse response function which is non-zero over an infinite length of time. This is in contrast to finite impulse response filters (FIR) which have fixed-duration impulse responses.

Recursive filters are signal processing filters which re-use one or more output(s) of the filter as inputs. This feedback results in an unending impulse response characterized by either exponentially growing, decaying, or sinusoidal signal output components.

IIR filters may be implemented as either analog or digital filters. In digital IIR filters, the output feedback is immediately apparent in the equations defining the output. Note that unlike with FIR filters, in designing IIR filters it is necessary to carefully consider 'time zero' case in which the outputs of the filter have not yet been clearly defined.

Design of digital IIR filters is heavily dependent on that of their analog counterparts which is because there are plenty of resources, and straightforward design methods concerning analog feedback filter design while there are hardly any for digital IIR filters. As a result, mostly, if a digital IIR filter is going to be implemented, first, an analog filter (e.g. Chebyshev filter, Butterworth filter, Elliptic filter) is designed and then it is converted to digital by applying discretization techniques such as Bilinear transform or Impulse invariance.

The difference equation of an IIR filter defining how the input signal is related to the output signal is as follows:

<!-- formula-not-decoded -->

where P is the forward filter order, b i are the forward filter coefficients, Q is the feedback filter order, a i are the feedback filter coefficients, x ( n ) is the input signal and y ( n ) is the output signal. A more condensed form of the difference equation is

<!-- formula-not-decoded -->

To find the impulse response we set x ( n ) = δ ( n ) where δ ( n ) is the Kronecker delta impulse. The impulse response for an IIR filter follows as

<!-- formula-not-decoded -->

The Z-transform of the impulse response yields the transfer function of the IIR filter

<!-- formula-not-decoded -->

We note that Z { δ ( n ) } = 1. Then with the definition of the impulse response and the time shift property of the Z-transform follows

<!-- formula-not-decoded -->

Stating all H ( z ) on the left hand side delivers:

<!-- formula-not-decoded -->

Isolating H ( z ) on the left hand side leads to the desired format of the transfer function

<!-- formula-not-decoded -->

The transfer function allows us to judge whether or not a system is Bounded-input, bounded-output stability (BIBO) stable. To find the poles of the transfer function, we can write equation 5.87 as follows:

<!-- formula-not-decoded -->

The poles of the IIR filter transfer function are the zeros of the denominator polynomial of the transfer function. The poles are evaluated as

/negationslash

<!-- formula-not-decoded -->

Clearly, if any a k = 0 then the poles are not located on the origin of the z-plane. This is in contrast to the Finite Impulse Response (FIR) filter where all poles are located on the origin of z-plane.

IIR filters are sometimes preferred over FIR filters because an IIR filter can achieve a much sharper transition region roll-off than an FIR filter of the same order.

## 5.3.6 Butterworth Filter

The Butterworth filter is one type of digital and electronic filter design. It is designed to have a frequency response which is as flat as mathematically possible in the passband. Another name for them is 'maximally flat magnitude' filters. The Butterworth type filter was first described by the British engineer Stephen Butterworth.

The frequency response of the Butterworth filter is maximally flat with no ripples in the passband, and rolls off toward zero in the stopband. When viewed on a logarithmic Bode plot, the response slopes off linearly toward negative infinity. For a first-order filter, the response rolls off at -6 dB per octave (-20 dB per decade). For a second-order Butterworth filter, the response decreases at -12 dB per octave, a third-order at -18 dB, and so on. Butterworth filters have a monotonically decreasing magnitude function with w . The Butterworth is the only filter that maintains this same shape for higher orders (but with a steeper decline in the stopband) whereas other varieties of filters (Bessel filter, Chebyshev filter, elliptic filter) have different shapes at higher orders. Compared with a Chebyshev Type I/Type II filter or an elliptic filter, the Butterworth filter has a slower roll-off, and thus will require a higher order to implement a particular stopband specification. However, Butterworth filter will have a more linear phase response in the passband than the Chebyshev Type I/Type II and elliptic filters.

Like all filters, the typical prototype is the low-pass filter, which can be modified into a high-pass filter, or placed in series with others to form band-pass and band-stop filters, and higher order versions of these.

The gain G ( ω ) of an n-order Butterworth low pass filter is given in terms of the transfer function H ( s ) as:

<!-- formula-not-decoded -->

where n = order of filter, c = cutoff frequency (approximately the -3dB frequency) and G 0 is the DC gain at zero frequency, figure 5.3.

It can be seen that for infinite values of n , the gain becomes a rectangle function and frequencies below ω c will be passed with gain G 0 , while frequencies above ω c will be suppressed. For finite values of n the cutoff will be less sharp.

We wish to determine the transfer function H ( s ) where s = σ + jω . Since H ( s ) H ( -s ) evaluated at s = jω is simply equal to | H ( ω ) | , it follows that:

<!-- formula-not-decoded -->

Figure 5.1. The gain of Butterworth low-pass filters of orders 1 through 5. The slope is 20 dB/decade where n is the filter order. Figure is adapted from [146]

<!-- image -->

The poles of this expression occur on a circle of radius ω c at equally spaced points. The transfer function itself will be specified by just the poles in the negative real half-plane of s . The k th pole is specified by:

<!-- formula-not-decoded -->

and hence,

<!-- formula-not-decoded -->

The transfer function may be written in terms of these poles as:

The denominator is a Butterworth polynomial in s .

The Butterworth polynomials may be written in complex form as above, but are usually written with real coefficients by multiplying pole pairs which are complex conjugates, such as s 1 and s n . The polynomials are normalized by setting ω c = 1. The normalized Butterworth polynomials then have the general form:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Assuming ω c = 1 and G 0 = 1, the derivative of the gain with respect to frequency can be shown to be:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

which is monotonically decreasing for all ω since the gain G is always positive. The gain function of the Butterworth filter therefore has no ripple. Furthermore, the series expansion of the gain is given by:

<!-- formula-not-decoded -->

In other words, all derivatives of the gain up to but not including the 2n-th derivative are zero, resulting in maximal flatness.

Again assuming ω c = 1, the slope of the log of the gain for large ω is:

<!-- formula-not-decoded -->

In decibels, the high frequency roll off is therefore 20n dB/decade. (The factor of 20 is used because the power is proportional to the square of the voltage gain.)

Here is an image showing the Butterworth filter next to other common kind of filters obtained with the same number of coefficients:

As is clear from the image, the Butterworth filter rolls off more slowly than all the others but it shows no ripples.

## 5.4 Wavelets

## 5.4.1 Development of Wavelet Theory

Mathematical transformations are applied to a signal to obtain further information, which is not readily available in its original time-domain form and which is more useful to the

Figure 5.2. A Comparison between Butterworth filter and other linear filters. Figure is adapted from [146]

<!-- image -->

application at hand. For example, in case of signal denoising, the best representation is the one in which the signal and the noise are easily separated. Fourier Transform (FT) is the oldest and the first of all transforms used in the history of signal processing. Joseph Fourier (1770-1830) first introduced the remarkable idea of expansion of a function in terms of a trigonometric series. In other word, he presented a new technique to decompose a signal into complex exponential functions of different frequencies. For a continuous signal x ( t ), The Fourier Transformation is defined as follows:

<!-- formula-not-decoded -->

The analysis coefficients, also called spectra X ( f ), are computed as inner products of the signal with sinusoidal basis functions of infinite duration. The trigonometric kernel exp ( -i 2 πft ), used here, oscillates indefinitely, and hence, the localized information contained in the signal x ( t ) gets lost. While the spectrum X ( f ) shows the overall strength with which any frequency f is contained in the signal x ( t ), it does not generally provide easyto-interpret information about the time-localization of spectral components. The analysis coefficients X ( f ) define the notion of global frequency f in a signal. However, time domain

and frequency domain constitute two alternative ways of looking at a signal. Although FT allows a passage from one domain to the other, it does not allow a combination of the two. This method enables us to investigate problems either in the time domain or in the frequency domain, but not simultaneously in both. Fourier transform theory has been very useful for analysing harmonic signals, or signals for which there is no need for local information. Fourier analysis is therefore an effective tool for studying stationary signals, that is, signals with time-independent frequency content. However, many of the practically encountered signals, like the ECG and most of the physiological signals, are non-stationary. A complete analysis of non-stationary signals requires a joint time-frequency representation. The basic idea of time-frequency representations of signals is to map a one-dimensional signal of time, x ( t ), into a two-dimensional function of time and frequency. Thus, they combine time-domain and frequency-domain analysis to yield a potentially more revealing picture of the temporal localization of a signal's spectral components. In order to incorporate both time and frequency localization properties in FT, Dennis Gabor in 1946 first introduced the windowed Fourier Transform or Short Time Fourier Transform (STFT). His major idea was to use a time-localization window function g ( t -τ ) for extracting local information from the Fourier transform of a signal. The parameter τ corresponds to the position of the window in time. τ is kept on varying to translate the window until the whole of time-domain is covered. The width of this window must be less or equal to the segment of the signal where stationarity is valid, that is, the distribution of the samples in that segment is similar to the distribution of the samples in any other segment.

<!-- formula-not-decoded -->

Although STFT overcomes the drawback of Fourier Transform apparently, it has got a serious problem related to the resolution in time and frequency. The root of this problem is related to Heisenberg's Uncertainty Principle , according to which exact time-frequency representation of a signal is not possible. Therefore, we can never know precisely which of the spectral components exists at what instants of time. What we can know is the time interval during which a certain band of frequency exists. A broader window gives better frequency resolution and poor time resolution. On the contrary, the time resolution can be improved at the cost of frequency resolution with shorter window. Once the window is chosen for STFT , the resolution in time and frequency domain gets fixed. However, many signals encountered in our practical life, especially in our case the ECG, requires a more flexible approach regarding this resolution. Wavelet transform (WT) was developed to overcome this fixed resolution problem of STFT . The Multiresolution Approach (MRA) in time and frequency domain, also called Multiresolution Signal Analysis, is the heart of WT. The basis of FT is sinusoidal waves of infinite, periodic smooth and predictable duration. On the other hand, WT decomposes signal into a set of compactly supported basis functions called wavelets or small waves, obtained from a single prototype mother wavelet by means of dilation and translation. On the contrary to FT, wavelets are a periodic, irregular and localized waves of finite energy. They have their energy concentrated in time or space and are suited to analyse a transient signal, which contains a high degree

of nonperiodic components and a higher magnitude of high frequencies than its harmonic contents, like ECG signals.

## 5.4.2 Multiresolution Signal Analysis

A signal can be viewed as the sum of a coarse part and a detailed part. The smooth part reflects the main features of the signal, therefore called the approximation signal, whereas the faster fluctuations represent the details of the signal. The separation of a signal into two parts is determined by the resolution, with which the signal is analyzed, i.e., by the scale below which no details can be discerned. A progressively better approximation of the signal is obtained by increasing the resolution so that finer and finer details are included in the smooth part [33]. The approximation of a signal x ( t ) at scale j is de-noted x j ( t ). At the next scale j + l , the approximation signal x j + i ( t ) is composed of x j ( t ) and the details y j ( t ) at that level such that

<!-- formula-not-decoded -->

By adding more and more detail to x j ( t ) we arrive, as the resolution approaches infinity, at a dyadic multiresolution representation of the original signal x ( t ) which involves a smooth part and the sum of different details,

<!-- formula-not-decoded -->

Unlike STFT which has a constant resolution at all times and frequencies, WT uses a Multi-Resolutional Approach (MRA), i.e. varying temporal resolution for different spectral components, which can be clarified as follows. Lower or narrower scales (higher frequencies) mean lesser ambiguity in time, i.e. good time resolution. Higher scales (lower frequencies) have wider support, leading to more ambiguity in time, or in other words, poor temporal resolution. The following figure compares the resolution for four different representations of the same signal.

The original time-domain signal has got no time resolution problem, since we know the value of the signal at every instant of time. In the Fourier transformed version, there is no resolution problem in the frequency domain, i.e. we know precisely what frequencies exist. Conversely, the frequency resolution in time domain and time resolution in Fourier domain are zero, since we have no information about them. For the two bottom diagrams, each box represents an equal area of the time-frequency plane, but different sized boxes giving different proportion to time and frequency.

All the boxes are of same size for STFT , i.e. the time and frequency resolutions are constant all over the time-frequency plane. For wavelet transform, at low frequencies (high scales), the height of the boxes are shorter (which corresponds to better frequency resolution, since there is less ambiguity regarding the value of the exact frequency), but their widths are longer (which correspond to poor time resolution, since there is more ambiguity regarding the value of the exact time). At higher frequencies (low scales), the width of the boxes decreases, i.e. the time resolution gets better, and height of the boxes increases, i.e. the frequency resolution gets poorer.

Figure 5.3. Time-Frequency Resolution at different signal representations. Figure is adapted from [146]

<!-- image -->

## 5.4.3 Continuous Wavelet Transform (CWT)

We start our exposition by recalling that the fundamental operation in orthonormal basis function analysis is the correlation, i.e. inner product, between the observed signal x ( n ) and the basis functions ϕ k ( n ), equation 5.19.

<!-- formula-not-decoded -->

The resulting coefficients w k define the series expansion of basis functions that describe x ( n ). In wavelet analysis, the two operations of scaling and translation in time are most simply introduced when the continuous-time description is adopted. Therefore, we mention the continuous-time version of the correlation in 5.104,

<!-- formula-not-decoded -->

A family of wavelets ψ s,r ( t ) is defined by scaling and translating the mother wavelet ψ ( t ) with the continuous-valued parameters s ( &gt; 0) and τ

<!-- formula-not-decoded -->

where the factor 1 √ s serves the purpose of energy normalisation of the wavelet across various scales, that is, assuring that all scaled functions have equal energy. Thus, the wavelet is contracted for s &lt; l, whereas it is expanded for s &gt; 1 [33]. The contraction of a wavelet to a smaller scale makes it more localized in time, while the corresponding frequency response is shifted to higher frequencies and the bandwidth is increased to become less localized in frequency; the reverse behavior is obtained when the wavelet is expanded in time.

The continuous wavelet transform (CWT) w ( s, T ) of a continuous-time signal x ( t ) is defined by the inner product of the signal x ( t ) and a scaled and translated version of a single prototype mother wavelet ψ ( t ), also called basis wavelet function,

<!-- formula-not-decoded -->

thus constituting a two-dimensional mapping onto the time-scale domain.

The CWT can be interpreted as a linear filtering Operation since 5.107 defines the convolution between the signal x ( t ) and a filter whose impulse response is 1 √ s ψ ( -t s ). The term translation is related to the location of the wavelet, as it is shifted through the signal x ( t ). This term corresponds to time information in the transform domain. Translating or shifting a wavelet means hastening or delaying its onset. The parameter scale in the wavelet analysis is similar to that used in maps. High scale gives a gross or global picture of the signal, whereas low scale corresponds to a detailed view. Similarly, in terms of frequency, low frequencies correspond to global information of a signal that usually spans the entire signal, whereas high frequencies correspond to detailed information of a transient pattern in the signal having relatively short duration. That is why scaling conveys a notion of something reciprocal to the frequency. Scaling, as a mathematical operation, either dilates or compresses a signal [33].

The function x ( t ) can be exactly recovered from w ( s, τ ) using the reconstruction equation [147]

where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and Ψ ( Ω ) denotes the Fourier transform of ψ ( t ). For the integral in 5.109 to exist, Ψ (0) must equal zero, i.e., the DC gain must be zero,

<!-- formula-not-decoded -->

Another requirement is that | Ψ ( Ω ) | must decrease to zero for | Ω →∞| . These two requirements imply that the wavelet function ψ ( t ) must have bandpass characteristics. Since the above requirements on the mother wavelet are relatively modest, it turns out to be a highly adjustable function which can be designed to suit various signal problems (this stands in sharp contrast to the Fourier transform where the basis functions are fixed once and for all).

## 5.4.4 The Dyadic Wavelet Transform (DyWT)

The CWT is a two-dimensional function W ( s, τ ) which is highly redundant. That is, CWT assigns a value to the continuum of points on the translation-scale plane taking a

long computing time. Therefore, it is necessary to discretize the scaling and translation parameters s and τ according to a suitably chosen sampling grid. Dyadic Wavelet Transform (DyWT) is based on sampling the translation-scale plane by using dyadic sampling of the two parameters,

<!-- formula-not-decoded -->

where j and k are both integer. Accordingly, the discretized wavelet function is defined by

<!-- formula-not-decoded -->

Inserting 5.112 into the CWT in 5.107, we obtain the dyadic wavelet transform (DyWT)

<!-- formula-not-decoded -->

It can be shown that with dyadic sampling it is still possible to exactly reconstruct x ( t ) from the coefficients w j,k resulting from discretization of the CWT; a coarser sampling grid cannot reconstruct x ( t ) [147]. From Nyquist's rule, we know that at higher scale (i.e. lower frequencies) the sampling rate can be reduced. In other words, if the translationscale plane needs to be sampled with a sampling rate of N 1 at scale s 1 , the same plane can be sampled with a sampling rate of N 2 at scale s 2 , where s 1 &lt; s 2 (corresponding to frequencies f 1 &gt; f 2 ) and N 1 &lt; N 2 [148]. The actual relationship between N 1 and N 2 is,

<!-- formula-not-decoded -->

Therefore, at lower frequencies, the sampling rate can be reduced saving a considerable amount of computation time. The original signal is retrieved by the inverse DyWT, or the wavelet series expansion

<!-- formula-not-decoded -->

where ψ j,k ( t ) is a set of orthonormal basis functions. In contrast to the series expansion of basis functions in 5.18, defined as the sum over one index, the wavelet series expansion is more flexible since it is the sum over two indices which are related to scaling and translation of the basis functions ψ j,k ( t ). Although DyWT has got computational efficiency over CWT, still it provides a high degree of redundancy as far as data reconstruction is concerned. This redundancy, on the other hand consumes a significant amount of computational resources. That is why we move on in this work to wavelet implementation based on digital filters, i.e. the Discrete Wavelet Transform (DWT), for discrete time signals, which is amazingly faster in operation.

## 5.4.5 Discrete Wavelet Transform (DWT)

Discrete Wavelet Transform (DWT) is described and implemented using the multiresolution signal approach which is expressed in equation 5.103 as follows:

<!-- formula-not-decoded -->

The scaling function ϕ ( t ) is introduced for the purpose of efficiently representing the approximation signal x j ( t ) at different resolution. On the other hand, it is desirable to introduce the function ψ ( t ), which complements the scaling function by accounting for the details of a signal, rather than its approximations.

## 5.4.5.1 The Scaling Function

This function can be used to generate a set of scaling functions defined by different translations,

<!-- formula-not-decoded -->

where the index '0' indicates that no time scaling is performed. The design of a scaling function ϕ ( t ) must be such that translations of ϕ ( t ) constitute an orthonormal set of functions,

<!-- formula-not-decoded -->

/negationslash

Therefore, the scaling functions ϕ 0 ,k ( t ) are said to span a subspace χ 0 of the whole space of square integral functions denoted L 2 ( R ),

<!-- formula-not-decoded -->

This subspace allows us to approximate x ( t ) to a signal x 0 ( t ) described as a linear combination of ϕ ( t ) at different translations ϕ ( t -n ),

<!-- formula-not-decoded -->

As before, the coefficients of the series expansion result from computing the inner product

<!-- formula-not-decoded -->

Analogously to dyadic sampling of the wavelet function ϕ ( t ), the scaling function in the equation 5.116 can be generalized through dyadic sampling to generate a set of orthonormal scaling functions for approximations at different resolution,

<!-- formula-not-decoded -->

where the factor 2 j/ 2 assures that the norm of ϕ j,k ( t ) is one for all indices j and k ,

<!-- formula-not-decoded -->

Orthonormality applies only to different translation indices k for a fixed scale j , and the scaling functions are thus not required to be orthonormal between different scales. With these basis functions, the approximation signal x j ( t ) is given by where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

It is important to realize that, for j &gt; 0, the span increases since ϕ j,k ( t ) contracts in time, thereby allowing details of x ( t ) to be better represented by the approximation signal x j ( t ). On the other hand, only the coarser information can be represented for j &lt; 0 since ϕ j,k ( t ) then expands [33].

The subspace χ j is spanned by ϕ j,k ( t )

<!-- formula-not-decoded -->

which has a time resolution only half as good as that of χ j +1 since the scaling function in χ j +1 is contracted by a factor of two, i.e., ϕ (2 j +1 t ) in relation to ϕ (2 j t ). As a result, the orthonormal basis functions that span χ j are also part of χ j +1 , and the multiresolution property is consequently described by a set of nested signal subspaces,

<!-- formula-not-decoded -->

Each subspace is spanned by a different set of basis functions ϕ j,k ( t ) , offering progressively better approximations such that x j ( t ) approaches x ( t ) in the limit as j →∞ ,

<!-- formula-not-decoded -->

where x ( t ) belongs to the space L 2 ( R ). An important relation is the refinement equation which relates ϕ ( t ), spanning χ 0 , to ϕ (2 t ), spanning χ 1 . Since these two signal subspaces are such that χ 0 ⊂ χ 1 , it is possible to express ϕ ( t ) as a linear combination of the shifted versions ϕ (2 t ),

<!-- formula-not-decoded -->

where h ϕ ( n ) is a sequence of scaling coefficients . As we will see later, the design of a wavelet function is synonymous with the selection of the coefficients h ϕ ( n ). The relation between scaling functions at different scales, as expressed by the refinement equation, will be used to develop a technique with which the series expansion coefficients can be calculated.

## 5.4.5.2 The Wavelet Function

A set of orthonormal basis functions at scale j is given by

<!-- formula-not-decoded -->

which spans the difference between the two subspaces χ j and χ j +1 . The functions ψ j,k ( t ) are related to the mother wavelet, introduced in the equation 5.106, and subjected to dyadic sampling. At scale j + l , the subspace describing signal details is given by

<!-- formula-not-decoded -->

where the wavelet functions that span ξ j are required to be orthonormal to the scaling functions of χ j ,

<!-- formula-not-decoded -->

for all indices j and k . As before, orthonormality is advantageous since it simplifies the calculation of the series expansion coefficients.

In the subspace χ j +1 , χ j is said to constitute an orthogonal complement to χ j which is denoted

<!-- formula-not-decoded -->

where ⊕ denotes the direct sum between two subspaces. Since 5.132 is valid for an arbitrary value of j , we also have that

<!-- formula-not-decoded -->

which, when continued until a certain value j 0 ( ≤ j ) is reached, yields the decomposition

<!-- formula-not-decoded -->

As j approaches infinity, the subspace decomposition can be expressed as

<!-- formula-not-decoded -->

where the detail signal y j ( t ) is determined by the detail coefficients d j ( k ), calculated as the inner product of x ( t ) and ψ j,k ( t ), where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Just as the scaling function ϕ ( t ) can be expressed as a linear combination of the shifted scaling functions with half the width, i.e., using the refinement equation in 5.128, the wavelet function ψ ( t ) can be similarly expressed by the wavelet equation

<!-- formula-not-decoded -->

The wavelet equation results from the property that ξ j ⊂ χ j +1 , which allows us to express ψ ( t ) in terms of shifted versions of ϕ (2 t ) similar to the procedure applied to ϕ ( t ) in 5.128. The coefficients h ψ ( n ) constitute a sequence of wavelet coefficients that differ from the scaling coefficients h ϕ ( n ). However, it can be shown that h ψ ( n ) can be determined from h ϕ ( n ) such that when the number of coefficients N ϕ is finite and even [149],

<!-- formula-not-decoded -->

where, n = 0 , . . . , N ψ -1. The two types of coefficients are thus the same except that every other coefficient has the opposite sign.

## 5.4.5.3 Discrete Wavelet Series Expansion

At the scale j 0 , the signal x ( t ) can be expressed as a wavelet series expansion in terms of the scaling coefficients c j ( k ) and the wavelet coefficients d j ( k ),

<!-- formula-not-decoded -->

Hence, x ( t ) can be decomposed into a signal x j 0 ( t ), being a lowpass approximation of x ( t ), and a set of signals y j ( t ) which gives varying degrees of high-resolution details of x ( t ). Furthermore, since the series expansion in 5.140 is expressed in terms of basis functions being mutually orthonormal, the coefficients c j 0 ( k ) and d j ( k ) are easily calculated by their corresponding inner products in 5.124 and 5.137, respectively. DWT is defined by the coefficients of the wavelet series expansion in 5.140. These coefficients can be viewed as the counterpart of the Fourier series coefficients; although their interpretation is no longer equally simple (i.e., no frequency interpretation) and the basis functions remain to be specified before the DWT can be calculated [33].

## 5.4.6 Implementation of the DWT Using Filter Banks

## 5.4.6.1 Analysis Filter Bank

An important reason for the popularity of multi-resolution analysis is the efficient calculation of the scaling and wavelet coefficients. This can be done with a set of recursive equations whose implementation involves well-known, basic signal processing operations (i.e., filtering and down- or upsampling). Starting with the refinement equation in 5.128,

<!-- formula-not-decoded -->

we have for an arbitrary scale j ,

<!-- formula-not-decoded -->

The equation 5.141 can be written also as:

<!-- formula-not-decoded -->

A recursive relation can be derived for the scaling coefficients c j ( k ) by multiplying both sides of 5.142 by x ( t ) and integrating to obtain the inner products,

<!-- formula-not-decoded -->

which yield the convolution,

<!-- formula-not-decoded -->

In an analogous manner, the wavelet coefficients d j ( k ) can be calculated by convolving the time-reversed coefficients h ψ ( -n ) with c j + i ( n ) and subsequent downsampling of the filtered output by a factor of two:

<!-- formula-not-decoded -->

The calculation of the coefficients c j ( k ) and d j ( k ) can be implemented using the twochannel analysis filter bank shown in figure 5.4- a , with which the coefficients at scale j are calculated from those at scale j +1. By repeatedly combining two-channel analysis filter banks to the output of h ϕ ( -n ), we obtain a dyadic tree structure which efficiently implements the DWT, see figure 5.4- b. It is important to realize that the scaling and wavelet functions do not explicitly appear in the calculation of the DWT, but only the scaling and wavelet coefficients are required. As a result, the output of the filter bank is a set of coefficients used to calculate the approximation and detail signals with 5.123 and 5.136, respectively [33].

Afrequency domain interpretation comes naturally for the filter parts of 5.144 and 5.145, which are defined by the scaling and wavelet coefficients, respectively. Although the filter h ϕ ( n ) is lowpass and h ψ ( n ) is highpass, but both filters have FIR filter structures. Having established these two filter characteristics, we realize that the analysis filter bank with its dyadic tree structure produces output signals which range from being highpass to lowpass, with various degrees of bandpass in between. The detail coefficients that result from bandpass filtering involve filters, whose center frequency gradually decreases due to the increasing number of lowpass filters h ϕ ( n ) being cascaded to the highpass filter to form the overall filter. The coefficients c 0 ( k ) which describe the approximation signal in subspace χ 0 are obtained by cascaded lowpass filters only.

With the requirement of h ϕ ( n ) being lowpass, the relation between the scaling and wavelet coefficients in 5.139 leads to the frequency function H ϕ ( e jw ) of h ϕ ( n ) being translated by π in order to yield H ψ ( e jw ),

Figure 5.4. The calculation of the DWT coefficients implemented using the two-channel analysis filter bank: a) A two-channel analysis filter bank for calculating the coefficients of the wavelet series expansion. b) The discrete wavelet transform based on the filter bank in (a), which, in this case, produces the coefficients that decompose the space χ 3 into χ 0 , ψ 0 , ψ 1 , and ψ 2 . Figures are adopted and adjusted from [33]

<!-- image -->

∣ ∣ H ψ ( e jw ) ∣ ∣ = ∣ ∣ H ϕ ( e j ( w + π ) ) ∣ ∣ , (5.146) and is thus a highpass filter. Because h ϕ ( n ) and h ψ ( n ) satisfy the condition in 5.146, they are called Quadrature Mirror Filters (QMF). Before the set of recursive equations can be used to produce c j ( k ) and d j ( k ), we must devise a technique for their initialization. It is, of course, necessary that x ( t ) enters the calculations; this applies in particular to its sampled counterpart x ( n ), invariably constituting the signal to be analyzed. For a fine enough scale j , one may argue that the scaling function has become so very narrow that the coefficients c j ( k ), which initialize the recursion, result from an inner product in which x ( t ] is multiplied by a delta function,

<!-- formula-not-decoded -->

Consequently, the signal samples x ( n ) themselves would serve as good approximations of the coefficients c j ( k ), provided that the signal x ( t ) has been sampled well above the Nyquist rate. Although this initialization procedure is the one which is normally used, other procedures exist which offer certain advantages [149]. Hence, the recursion is initialized with the sampled signal x ( n ), whose length is finite and given by N. Due to the very dyadic nature of the algorithm, it is natural to assume that the length is a power of two, i.e., N = 2 J . Accordingly, J + l different scales can be analyzed, of which the finest scale is j = J and described by N coefficients (i.e., the signal itself), while the coarsest scale is j = 0 with only one coefficient. The calculation of the DWT through successive decomposition of the approximation coefficients is illustrated in figure 5.5, where the finest resolution is given by the scale j = 3. The procedure is initialized by setting the approximation

coefficients c 3 ( k ) equal to the signal samples x ( n ). In this example where x ( n ) has a length of N = 8, the DWT is given by the coefficients c 0 (0) , d 0 (0) , d 1 (0) , d 1 (1) , d 2 (0) , d 2 (1) , d 2 (2) , and d 2 (3). Thus, the resulting number of coefficients is identical to the length of the signal [33].

Figure 5.5. The calculation of the DWT through successive decomposition of the approximation coefficients: the calculation of the DWT coefficients implemented using the two-channel analysis filter bank: Calculation of the DWT for a signal of length N = 8. The final result is given by the coefficients at the bottom for j = 0. The vertical arrows indicate that the coefficients are simply copied down from the previous scale. The calculation is initialized by setting the coefficients c 3 ( k ) equal to the signal samples x ( k ). Figure is adopted and adjusted from [33]

<!-- image -->

## 5.4.6.2 Synthesis Filter Bank

While the analysis filter bank decomposes the signal into a set of coefficients at different resolution, the purpose here is to perform the reverse operation of merging the coefficient sequences so as to implement the inverse DWT. The inverse transform can also be implemented with a filter bank, but with a structure that differs slightly from the one which implements the DWT. In order to derive a set of equations which recursively determine c j + ( k ) from c j ( k ) and d j ( k ), we start by expressing the approximation signal x j +1 ( t ) as a linear expansion of the scaling function at scale j + l

<!-- formula-not-decoded -->

Relying on the decomposition in 5.132, stating that χ j +1 = χ j ⊕ ξ j , we can alternatively express x j +1 ( t ) at scale j ,

<!-- formula-not-decoded -->

Now, making use of the scaling and wavelet equations in 5.128 and 5.138, respectively, we obtain

<!-- formula-not-decoded -->

By multiplying both sides of 5.150 by ϕ j +1 ,k ( t ) and integrating to obtain the inner products, the following recursion is obtained for c(k),

<!-- formula-not-decoded -->

Alternatively, this equation can be expressed as

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and d u j ( k ) is defined analogously to c u j ( k ). Hence, the two sums in 5.151 can be interpreted in terms of upsampling by a factor of two, i.e., by inserting zeros as every other input sample, and filtering so that the calculation of the coefficients c j +1 ( k ) is implemented by the two-channel synthesis filter bank shown in figure 5.6- a. By repeatedly combining two-channel synthesis filter banks to merge signals at different resolutions, we obtain a dyadic tree structure which implements the inverse DWT, see figure 5.6- b. The filters involved in the synthesis filter bank are the same as those used in the analysis filter bank, but with their impulse response reversed in time. In practice, there is always a maximum scale J with a resolution so fine that the wavelet (detail) coefficients can be neglected. Therefore, the wavelet series expansion in 5.140 may be replaced by

<!-- formula-not-decoded -->

thus indicating the coefficients that must be calculated with 5.151 to obtain x ( t ) (recall from the equation 5.147 that x ( k ) ≈ c j ( k ) for a sufficiently fine scale). Finally, we note that x ( t ) can be expressed as a series expansion solely in terms of the wavelet functions when c j for j 0

0 →-∞ →-∞

<!-- formula-not-decoded -->

where

Figure 5.6. The dyadic tree structure implementing the inverse DWT: a) A two-channel synthesis filter bank. b) The inverse discrete wavelet transform based on the filter bank in (a) which, in this case, produces the coefficients of the space χ 3 based on χ 0 , ψ 0 , ψ 1 , and ψ 2 . Figures are adopted and adjusted from [33]

<!-- image -->

which becomes the definition of the inverse DWT in 5.115, but with truncation of scales with negligible coefficients [33].

## 5.4.6.3 Subband Coding and DWT

DWTdecomposition halves the time resolution, since only half the number of samples now characterizes the entire signal. However, this operation doubles the frequency resolution, since the frequency band of the signal now spans only half the previous frequency band, effectively reducing the uncertainty in the frequency by half. This procedure, which is also known as the subband coding, can be repeated for further decomposition. At every level, the filtering and subsampling will result in half the number of samples (and hence half the time resolution) and half the frequency band spanned (and hence doubles the frequency resolution).

The frequency band of the signal is always from zero to the highest frequency in the signal f max , which is equal to the half of the sampling frequency f s referring to Nyquist Shannon sampling theorem as follows:

<!-- formula-not-decoded -->

By normalizing the sampling frequency f s to 1. The maximum angular frequency, which corresponds to f max , is equal to π (rad/s) in the frequency domain and the subband coding algorithm will span the frequency band of zero to π (rad/s). At the first decomposition level, the signal is passed through the highpass and lowpass filters, followed by subsampling by 2. The output of the highpass filter has half the time resolution, but it only spans the frequencies π/ 2 to π (rad/s), hence doubling the frequency resolution. The output of the lowpass filter also has half the time resolution, but it spans the other half of

the frequency band, frequencies from 0 to π/ 2 (rad/s). This signal is then passed through the same lowpass and highpass filters for further decomposition. The output of the second lowpass filter followed by subsampling has half the time resolution of the previous level spanning a frequency band of 0 to π/ 4 (rad/s), and the output of the second highpass filter followed by subsampling has also half the time resolution of the previous level, but spanning a frequency band of π/ 4 to π/ 2 (rad/s). The second highpass filtered signal constitutes the second level of DWT coefficients. This signal has half the time resolution, but twice the frequency resolution of the first level signal. In other words, time resolution has decreased by a factor of 4, and frequency resolution has increased by a factor of 4 compared to the original signal. The lowpass filter output is then filtered once again for further decomposition. This process continues until two samples are left. The DWT of the original signal is then obtained by concatenating all coefficients starting from the last level of decomposition. The DWT will then have the same number of coefficients as the original signal.

## 5.4.7 Properties of DWT Orthogonal Wavelet

Although the scaling function ϕ ( t ) is not explicitly required for calculation of the DWT, it is nevertheless important to assess whether its properties are suitable or not. One approach to calculating ϕ ( t ) from h ϕ ( n ) is to insert the scaling coefficients into the refinement equation, but now modified into an iterative algorithm,

<!-- formula-not-decoded -->

where i denotes the iteration index. This algorithm, known as the cascade algorithm, produces successive approximations of ϕ ( t ) so that ϕ i ( t ) approaches ϕ ( t ) as the iteration index i increases. If the algorithm converges, the Fourier transform Φ ( Ω ) of ϕ ( t ) can be related to the scaling coefficients h ϕ ( n ) by iteratively applying the Fourier transform to 5.157,

<!-- formula-not-decoded -->

where H ϕ ( e jΩ ) denotes the discrete-time Fourier transform of h ϕ ( n ) and is a periodic function. Using the wavelet equation in 5.138, the Fourier transform Ψ ( Ω ) of the wavelet ϕ ( t ) can be expressed as

<!-- formula-not-decoded -->

Since ϕ ( t ) is assumed to have lowpass characteristics, the factor Φ (0) can be normalized such that

<!-- formula-not-decoded -->

Hence, the outcome of the cascade algorithm in 5.157 depends only on the properties of the scaling coefficients and not on the shape of the initial ϕ (0)( t ) , except the factor Φ (0) which is invariant over the iterations.

## 5.4.7.1 Smoothness and Vanishing Moments

The moments of an orthogonal wavelet m k , defined by

<!-- formula-not-decoded -->

vanish up to a certain value k = K ψ . Alternatively, the moment definition in 5.161 can be expressed in terms of its Fourier transform

<!-- formula-not-decoded -->

which establishes that vanishing moments are synonymous with K ψ derivatives of Ψ ( Ω ) at DC, i.e., Ω = 0, being equal to zero. This requirement implies that ψ ( t ) is smooth and may, if desired, be extended to embrace ϕ ( t ) as well. Another consequence of vanishing wavelet moments is that the inner product between a polynomial signal x ( t ) = ∑ k a k t k and ψ ( t ) is zero, and thus the detail coefficients are zero. As a result, polynomial signals are well-represented by the approximation coefficients, and the detail coefficients can be discarded.

The smoothness of wavelets plays an important role in compression applications. Compression is usually achieved by setting small coefficients to zero and thus leaving out a component from the original function. If the original function represents an image for instance, and the wavelet is not smooth, the error can easily be detected visually.

<!-- formula-not-decoded -->

## 5.4.7.2 Compact Support

The scaling function and wavelet function have compact support, when h ϕ ( n ) and h ψ ( n ) are finite impulse response filters (FIR), so that they are trigonometric polynomials. In other words, wavelets will have compact support, when its scaling function and wavelet function have a duration which is limited in time. If the scaling function and wavelet are symmetric then their filters have linear phase. The absence of this property can lead to phase distortion, which is important in signal processing applications.

## 5.4.7.3 Orthogonal Wavelet Bases

- The Daubechies wavelets : Each wavelet in Daubechies family has a number of zero moments or vanishing moments, µ k , equal to half the number of coefficients, K ψ = N ψ / 2 moments [150]. As K ψ increases, both the wavelet function and the scaling function become increasingly smooth. A disadvantage of the members of this family is

their highly asymmetric shape. Daubechies orthogonal wavelets D2-D20 (even index numbers only) are commonly used. The index number refers to the number N of coefficients. For example D2, the Haar wavelet, has one vanishing moment, D4 has two moments, etc. Daubechies filters length is equal to 2 N ψ , whereas support width is 2 N ψ -1. A vanishing moment refers to the wavelets ability to represent polynomial behaviour or information in a signal. For example, D2, with one moment, easily encodes polynomials of one coefficient, i.e. constant signal components. D4 encodes polynomials of two coefficients, i.e. constant and linear signal components. The Haar wavelets offer the advantage of being very well-localized in time (compact support). Haar wavelets constitute a set of shifted and scaled square wave functions, suitable for defining scaling and wavelet functions [151]. The Haar scaling function is defined as

<!-- formula-not-decoded -->

Haar scaling functions span different subspaces and satisfy the orthonormality condition. Furthermore, they are solutions of the refinement equation with two nonzero coefficients,

<!-- formula-not-decoded -->

The corresponding Haar wavelet function, shown in figure 5.7, is required to be with two nonzero coefficients

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The scaling and wavelet functions are orthonormal.

Daubechies proposes modifications of her wavelets that increase their symmetry while retaining great simplicity. The modified Daubechies wavelets are called Symlet wavelets. The other properties of Symlet wavelets are similar to those of the Daubechies wavelets.

- The Coiflets wavelets : They constitute another wavelet family with compact support, but designed such that N ψ / 3 -1 moments of the scaling function and K ψ = N ψ / 3 of the wavelet vanish. Coiflets filters length is equal to 6 N ψ , whereas their support width is 6 N ψ -1. Coiflets filters length and support width are obviously larger than those of Daubechies wavelets. Coiflets are more symmetric than the Daubechies wavelets, a property that comes at the price of an increased filter length. Therefore, it is obvious that Coiflets are superior in producing smooth approximations when compared to Daubechies wavelets.

Figure 5.7. The Haar Wavelet Function. Figure is adapted from [152]

<!-- image -->

There are many other types of wavelets available in addition to those mentioned here, with each exhibiting its particular advantages.

## 5.4.7.4 Biorthogonal Wavelet Bases

In biomedical signal processing, it is often desirable to have symmetric wavelets. However, scaling functions and wavelets cannot, in general, accommodate this property since they are required to be orthogonal with exception to the Haar wavelet. By softening the orthogonality requirement between analysis and synthesis filters to, what is called, biorthogonality [153], it is possible to design symmetric wavelets which still implement the DWT and its inverse (IDWT).

## 5.4.8 Discrete Stationary Wavelet Transform (SWT)

In fact, the classical DWT is not a time-invariant transform. Therefore, the stationary wavelet transform (SWT) restores the translation invariance as a desirable property lost by the classical DWT. The signal is never downsampled or upsampled at any decomposition level when using SWT decomposition and ISWT reconstruction; so that each set of coefficients (details or approximation) contains the same number of samples as the input signal. The general step j , for example, convolves the approximation coefficients at level j -1, with upsampled versions of the appropriate original filters by the factor of 2, to produce the approximation and detail coefficients at level j . Although the main application of the SWT is de-noising [154], SWT do have other several useful applications such as breakdown points detection. SWT can be only defined for signals of length divisible by 2 J , where J is the maximum decomposition level.

## 5.4.9 Discrete Wavelet Packets Transform (DWPT)

DWPT represents a powerful generalization of the DWT [155]. While the DWT successively decomposes the scaling coefficients c j ( k ) which define the approximation signals

at different scales, the DWPT successively decomposes both the scaling coefficients c j ( k ) and the wavelet coefficients d j ( k ) which define the detail signals. As a result, the DWPT produces N coefficients at each scale, whereas the DWT produces a total of N coefficients. From the different scales of the wavelet packet decomposition, a total of K , out of N , coefficients are selected to represent the signal in the transform domain.

Like the DWT, the DWPT can be implemented by the filter bank with highpass and lowpass filters. However, decomposition of both scaling and wavelet coefficients means that the output of each branch of the filter bank is split into lowpass and highpass filters. Therefore, the dyadic tree structure of the DWT is replaced by a binary structure with one two-channel filter bank at the first stage, two two-channel filter banks at the second stage, four two-channel filter banks at the third stage, and so on. The selection of DWPT coefficients is often based on an information measure, like entropy, which concentrates as much information in as few coefficients as possible. Another approach is to select the coefficients so that a distortion measure does not exceed a certain error tolerance [156].

## State of the Art In ECG Signal Processing

## 6.1 Baseline Wander

Several methods have been proposed in the literature to eliminate baseline wander. The first is ensemble averaging. However, this approach is not a realistic one as the ECG signal exhibits beat-to-beat variations. A second widely used method is the polynomial interpolation as a linear and time-variant filtering technique. Linear interpolation introduces significant distortions. A third order approximation called cubic spline [157] is proved to give better results. Interpolation techniques make use of a previous knowledge of the ECG namely isoelectric levels estimated from the PR intervals, also called knots. Therefore, the performance of this technique depends highly on the knots determination accuracy and gets degraded as the knots become more separated in time, like the case with low heart rate. To overcome the above problem, another group proposed digital narrow-band linear-phase time-invariant filtering [158]. This method can be implemented in real time, but has two major draw-backs. First, the filter needs to be a FIR filter with a long impulse response, which means a large number of coefficients. Secondly, given that ECG and baseline wander spectra usually overlap, it is not possible to remove baseline wander without distorting ECG. Another technique has been proposed in [159] which uses a time-varying linear filter that selects different cut-off frequencies as a function of the heart rate or the baseline level. This filter improves the time invariant FIR filter performance, but can yet distort the ST components of ECG and has high computational requirements. Another group employed Short Time Fourier Transform (STFT) to get rid of baseline drift [160]. Within every window, they search for a spectral component in the range of DC to 1.0 Hz. Only the ECG segments containing frequency components in the specified range are high-pass filtered to cancel baseline wander. However, it is not possible to have optimal frequency and time resolution at the same time with STFT. Adaptive filtering has also been proposed to cancel the baseline drift [161]. An adaptive transversal filter with only one weight is used, where the reference input is a constant with a value of 1 and the primary input is the ECG signal. This filter, using the Least Mean Square (LMS) Algorithm in the adaptation process, is equivalent to a linear notch filter, that takes the advantage of adaptive implementation, but still modifies the ST segment. In [162], a cascade adaptive filter has been used. The first stage of the filter is exactly similar to that mentioned above. In the second stage, the primary input is the output from the first stage and the reference input is a unit impulse sequence correlated with each QRS complex. This method needs

a QRS detector in order to generate the impulse sequence. However, in our application baseline wander cancellation is accomplished as a pre-conditioning of ECG signal before delineation. The last group proposed a new algorithm for the removal of the baseline wander in ECG signal based on the wavelet packets method. The energy of the signal for both the coarse and detail levels is calculated in each scale. These energies represent the energy of the decomposed signal in assumed scale. The next step is to compare them and then choose the branch of the wavelet binary tree that has the higher energy. The higher energy branches will be followed until a point is reached where energy difference exceeds a preset threshold level. At this point the binary tree is complete, and the baseline wander signal is identified. Using the wavelet coefficients obtained, the inverse wavelet transform is calculated. In wavelet domain the baseline wander is subtracted from original data record and a baseline wander free ECG signal is identified [163]. It is actually very crucial to define a suitable and precise threshold that can find the optimal wavelet tree, since both ECG and baseline wander signals have various number of morphologies and since baseline wander may include different forms of electrode drift signal in different amplitude. Furthermore, it is a very time-consuming method, particularly when we deal with high-resolution, multi-channel and ambulatory monitoring ECG signals.

## 6.2 ECG Segmentation and Fiducial Points Detection

Automatic ECG segmentation methods, ECG delineation techniques or QRS detection algorithms, have been and still are subject of major importance in research for more than 30 years. ECG segmentation, also called fiducial points detection, is very important in computer-aided ECG analysis, especially in case of arrhythmia. A usual arrhythmia system consists of the following steps: 1) the removal of noise and artifacts 2) fiducial points detection 3) morphological classification 4) the rhythm analysis and medical interpretation. One can find in the literature many different QRS complex detection and ECG delineation approaches based on mathematical models, like Pan Tompkins algorithm, adaptive filters, artificial neural networks or hidden Markov models, wavelet transform, signal envelope, matched filters, ECG slope criteria, second-order derivatives, the , nonlinear time-scale decomposition. They will be described in details in the following sections.

## 6.2.1 QRS Complex Detection Algorithms

In order to be clinically useful and able to follow both sudden and gradual changes of QRS morphology, a QRS detector must be able to detect a large number of different QRS morphologies and it must not be limited to certain types of rhythm. A QRS detector is designed to detect heart-beats. QRS complex is generally used as a reference within the cardiac cycle. Most QRS detectors consists, in general terms, of three main blocks as follows [164]:

1) The linear filter : it is designed to have bandpass characteristics such that the essential spectral content of the QRS complex is preserved, while unwanted EGG components such as the P and the T waves are suppressed. The center frequency of the filter varies from 10 to 25 Hz and the bandwidth from 5 to 10 Hz [165]. Therefore, the linear filtering in

the preprocessing stage of the QRS detection algorithms generally consists of a high-pass filter in order to attenuate other signal components and artifacts, such as P-wave, T-wave and baseline drift whereas uncoupling noise is usually suppressed with a low-pass filter. In contrast to other types of ECG filtering, waveform distortion is not a critical issue in QRS detection. The focus is instead on improving the SNR to achieve good detector performance [33].

- 2) The nonlinear transformation : It transforms each QRS complex into a single positive peak better suited for threshold detection.

3) The decision rule : it takes the output of the nonlinear transformation or the linear filter and checks whether a QRS complex is present or not. The decision rule can be implemented as a fixed or adaptive amplitude threshold procedure, but may also include additional tests. A wide diversity of algorithms has been proposed in the literature for QRS-complex detection using different decision rules for the reduction of false-positive detections.

Pan Tompkins algorithm [166], also called the low-pass differentiation algorithm (LPD), consists of two major stages, i.e. the preprocessing and the decision levels. In the preprocessing stage, the ECG signal is first filtered with a bandpass filter in the range 5-15 Hz reducing the high-frequency and the low-frequency interference. The slope information of the QRS complex is provided then by applying a derivative procedure or operator. Afterward, a squaring operator is employed making all data points positive. The nonlinear amplification is emphasizing the large values from QRS complexes and suppressing the small values from P and T-waves. The output of the squaring operation has multiple peaks. Therefore a moving-window integration filter is applied on that output. The window size should be approximately in the same length of QRS complex in order to prevent peaky result in case of narrow window and to prevent T wave to merge with QRS complex in case of wide window. The decision stage in Pan Tompkins algorithm employees two thresholds to detect R peaks. The first threshold is calculated from the adaptive average value of noise peaks and QRS peaks as well as a threshold factor. Whereas, the second search-back threshold is a proportion of the first one. In this stage, a search-back procedure is developed in order to decrease the number of missed QRS complexes. His adaptive and a refractory time rule is used to decide between two QRS complexes or more, which are within a physiologically impossible short distance of each other. Pan Tompkins algorithm has serious difficulties guaranteeing a reliable detection of R position in normal QRS complex and in PVCs. The time-domain bandpass filter in this algorithm needs to follow hard conditions, namely a linear phase response and long impulse response with large number of coefficients, to provide a good subbanding for QRS complex detection.

Adaptive filters have been used to give an estimate of the current ECG sample as a weighted sum of previous ECG samples. The weights in the sum are updated according to the changing signal statistics. Sharp changes in the weights and in the errors of the current ECG sample estimate were used as features for QRS complex detection [167]. Neural networks, trained to be adaptive non-linear predictors of the ECG signal, have been used in [168, 169] for QRS complex detection.

In [170, 171, 172, 173], Dyadic Wavelet Transform (DyWT) has been proposed. In [172], only the QRS complex detection is accomplished as they are more interested in the heart

rate variability. They made use of the property that the absolute value of DyWT has localized maxima across several consecutive scales at the instant of occurrence of transients. Applying a definite threshold criterion, the peaks are located in a particular scale. Then the next higher scale is scanned in the same way. If the number of peaks in both cases does not agree, computation is carried out for the next scale. Finally, for acceptance as QRS locations, three consecutive scales should agree on the same number of peaks and also the corresponding peak locations in different scales must be within tolerable time deviation. In [173], an on-line QRS detection algorithm was developed based on the Haar Wavelet and implemented as a recursive filter. They also use magnitude threshold to determine the location of R peaks. In [170, 171, 172], a spline wavelet, a derivative of the Gaussian smoothing function, has been used as the prototype mother wavelet. The implementation is carried out by means of digital filters, also called filter banks. The WT at a particular scale is proportional to the derivative of the filtered version of the signal with a smoothing impulse response at that scale. Therefore, the zero-crossings of the WT correspond to the local maxima or minima of the smoothed signal at different scales, and the maximum absolute values of the WT are associated with maximum slopes in the filtered signal. In [170], modulus maximum lines corresponding to R waves are first searched across four different scales, namely, 2 1 , 2 2 ,2 3 and 2 4 , using different threshold for different scales , which is based on the corresponding RMS value. For a valid R wave, the Lipschitz regularity [165] must be greater than zero. Also, the R wave corresponds to a positive-maximum negative-minimum pair at each characteristic scale. After applying certain definite criteria, the isolated and redundant modulus maximum lines were rejected. Finally the R peaks were located at the zero-crossing points between the positive maximum-negative minimum pairs at scale 2 1 . In [170, 171], protection rules, like refractory period or search back routine, are included. Other approaches include cross-correlation methods, where a QRS complex template is aligned to the ECG signal [174]. Other syntactic approaches are used, where the ECG signal is represented as a piecewise linear approximation, and is analysed using syntactic rules [175, 176]. An extensive review of QRS complex detection approaches proposed in the last decade can be found in [165]. The large variation in the QRS complex morphologies as well as the various form and level of noise challenge all automatic detection algorithms, so that further performance improvements are still an important goal of current research.

## 6.2.2 Delineation Algorithms

Goal of the delineation algorithms is to find the QRS, P and T-wave boundaries to allow some quantitative measurements. There is so far no universal and clear rule to define the onset and the offset of ECG waves and complexes, but the hope of automatic delineation algorithms is still in getting a new standard in locating the boundaries of those waves and complexes. Delineation algorithms usually depart from a previous detected QRS location, namely R peak. Lots of work has been done in the field of ECG delineation using Wavelet Transform .

The QRS delineator in [170, 171] before and after the result of the QRS detector, the R peak, in the second scale for significant maxima and minima that can exceed a 'significant threshold'. The zero crossings between these significant slopes are assigned to wave peaks, and labeled depending on the sign and the sequence of the maximum - minimum pairs.

The onset of the QRS complex is considered before the first significant slope, whereas the offset is after the last significant slope. Possible onset and offset positions are determined by two criteria. The first considers the position of onset and offset of QRS complex where the signal is below a certain threshold taken with respect to the amplitude of the maximum. The next criterion localizes the boundaries of the QRS complex where the position of a local minimum before the first peak and after the last peak associated with the QRS complex. Finally the QRS onset and end are selected as the candidates that supply the nearest sample to the QRS complex. New in the algorithm described by [171] with respect to [170] is the detection and identification of the QRS individual waves. Any possible QRS morphology with three or less waves (QRS, RSR', QR, RS, R and QS complexes) are considered. The method includes protection measures based on time interval and sign rules, to reject notches in waves and anomalous deflections in the EGG signal.

The algorithm of T-wave detection and delineation in [170, 171] begins with defining a search window for each beat, relative to the QRS position and depending on the RRinterval. Within this window, local maxima and minima are detected in the fourth scale. If at least two exceed the threshold for T-wave detection, a T-wave is considered to be present. In this case, the local maxima and minima with amplitude greater than a second threshold (significant threshold) are considered as significant slopes of the wave and the zero crossings between them as the wave peaks. Depending on the number and polarity of the found extrema, in [171] one out of six possible T-wave morphologies were assigned. The possible waves are positive monophasic, negative monophasic, only upwards, only downwards, positive/negative biphasic or negative/positive biphasic.

If the T-wave is not found in the first chosen scale the above process is repeated over the next higher scale. To identify the wave limits, the same criteria as used for detecting the QRS onset and offset, with a third kind of thresholds were used. The P-wave detection and delineation algorithm is similar to the T-wave algorithm, except that the possible P-wave morphologies that the delineator can work with are four, including positive monophasic, negative monophasic , positive/negative biphasic or negative/positive biphasic.

In total there are 16 different thresholds which are used for the QRS complex, P and T-wave delineation. They can be grouped into three types. Six thresholds to decide if a pair of extrema with opposite sign can account for a wave (4 for QRS detection and one for T and one for P-wave delineation). These thresholds are proportional to the root mean square (RMS) value of the DyWT at the corresponding scales where the RMS is measured in each interval between two consecutive QRS complexes.

The second type of thresholds contains 4 thresholds and they are used to determine if the amplitude of the local maximum and minimum are significant. These thresholds are related to the amplitude of the global extrema within the corresponding search window. The last six thresholds belonging to the third group and are used to determine the onsets and offsets of QRS complex, T and P waves and are proportional to the amplitude of the DyWT at the first (last) maximum (minimum) of the complex or wave.

In [171], the same procedure of [170] is extended and evaluated on several manually annotated databases. They also generalize the filter coefficients (for DyWT) for different sampling frequencies of the ECG. Moreover, they considered more morphological variations for T wave in addition to those listed in [170].

The localization of wave onsets and ends is difficult, because the signal amplitude is low at the wave boundaries and the noise level will be higher than the signal itself. Therefore [177] suggested to improve the T and U-wave (TU-complex) delineation in a two stage process, where the ECG segment after the QRS-complex is first modeled by a mathematical model. The mathematical model consist of four 'action potential models' (AP-models), where the modeling of the APs is limited to the second half of the AP, because only the TU-complex is modeled. Once the model parameters for both waves are determined, the wave boundaries are determined using the derivative and thresholds.

A description of an LPD delineation algorithm has been given in [178]. The preprocessing stage of the LPD delineation algorithm always processes the ECG signal with a low pass filter and a differentiator. For the QRS start boundary detection the ECG signal after the low pass filter and the first differentiator is taken. The R-peak is assumed to occur at a maximum in the ECG signal and otherwise, the signal is inverted. The R-peak is thus a zero crossing of the derivative signal. First step is finding the next large local maximum to the left of the R-peak as well as the next local minimum to the left of this maximum. Determination of the start of the QRS-complex is depending on the relative positions of the first zero crossing and the first local minimum to the left of the maximum. The QRS end boundary detection is done similar except that maxima and minima are looked for in the second derivative. T-wave detection and delineation is done in a search window after a detected QRS-complex. The boundaries of the window are calculated depending on the actual heart rate. The maximum and minimum of the differentiated signal are found in the window of interest. Depending on the combination of the extrema and their sizes, four possibilities of different T-wave shapes are considered: upward-downward shape, downward-upward shape, downward shape and upward shape. The P-wave is searched for within a window before a detected QRS-complex. The maximum and minimum of the differentiated signal are found in the window of interest. In the implemented system, it is assumed that the P-wave is 'upward-downward' in shape. The left boundary is the position where the differentiated signal drops below a fraction offset max value, and the right boundary is the position where the differentiated signal rises above a fraction offset min value. If this does not happen in the window, no P-wave will be found.

In fact, the LPD delineation algorithm has serious technical and structural drawbacks. A bad threshold update and a too simple R peak detection method as well as only supporting for the standard QRS morphology are some of the technical drawbacks. The delineator shows structural problems by missing the detection of low frequency component QRS complex (PVCs for example), by dealing with different morphologies and by facing difficulties optimizing the algorithm parameter. The work in [141] has improved the performance of the LPD delineation algorithm by adjusting the technical and structural cores of the delineator. In this work, every new detected complex or wave is compared to the already detected complexes or waves by means of the cross-correlation coefficients in a so-called verification system section. The new method adjusted the threshold update rules in a better way than the conventional Pan Tompkins algorithm and it allowed more accurate peak detection, namely R peaks, by considering different QRS morphologies. Improvements in P and T-wave delineation are also noticed. However, problems and difficulties still exist in the verification system part due to the amount of possibilities how the

waves and complexes can vary within one morphology group. Beside the different possible morphologies the waves can vary in amplitude as well as in width. In order to fix this problem, implementing a modulation of the templates in term of width and amplitude was suggested, but it would further increase the computational load. Another main drawback is the long computational time needed, especially when dealing with ambulatory or multi-channel ECG signals.

A completely different approach using artificial neural networks can be found in [179], where a 2-layer perception neural network is trained, to determine T offsets. The weights of the network are estimated during the Bayesian motivated training process. Another approach which contains a training phase is the use of hidden Markov models which has been used in [180, 181]. The hidden Markov model comprises out of the following sates: P-wave, QRS-complex, T-wave, U-wave and Baseline. The model is trained in a supervised manner, where the transition matrix parameters were computed using the maximum likelihood estimates.

A new, computationally quite simple algorithm for T wave end location in the ECG is proposed in [182]. It mainly consists of the computation of an indicator related to the area covered by the T-wave curve, which can be implemented as a simple finite impulse response (FIR) filter. Based on simple assumptions, essentially on the concavity of the T-wave form, it has been proved that the maximum of the computed indicator inside each cardiac cycle coincides with the T-wave end.

Further delineation approaches one can find in the literature are referenced in [171] and include the signal envelope [183], matched filters [184], ECG slope criteria [185, 186, 187], second-order derivatives [188], non-linear time-scale decomposition [189], adaptive filtering [190] and dynamic time warping [191].

Not all of the algorithms presented above are able to localize all ECG characteristic points.

## 6.3 PCA Applications on ECG Signal

In 1981 Lux et al. has used the Karhunen-Lo` eve Transform (KLT), which is equivalent to PCA, as a method of quantitatively characterizing 192 lead body surface potential maps from 124 normal subjects and 97 patients [140]. Each map frame in QRS and ST-T of 34 maps in a test set was represented as a linear sum of orthonormal distributions (PCA coefficients) derived from the covariance matrix and estimated from all QRS frames in the 221 training maps. Results suggested that 12 independent waveforms, derived from the 192 measured ECGs, may be used in place of those 192 ECGs. In the literature, PCA has also been used to reduce the data dimensionality while performing ECG data compression, either alone or combined with other techniques as Self-Organizing Maps (SOM) [192, 193, 194, 195]. Furthermore, It is applied as a powerful tool for pattern recognition and linear feature extraction of QRS complex and ST-T morphology [196, 197, 198, 199], as well as ECG data clustering [200, 201]. Moreover, PCA ratio, which is quantified by the ratio of the second to the first eigenvalue of PCA, has been defined as an index of complexity of T wave loop morphology in 12-lead ECG and used as predictor of cardio-

vascular mortality [202, 203].

M. Zabel et al. derived five aspects from Singular-Value-Decomposition (SVD) of the Twave in vector cardiography. The latter is a technique based on at least 12 electrodes and therefore not directly comparable to the ones used in the present thesis. Their intention was to quantify the susceptibility to sudden cardiac death in a population of post myocardiac infarction subjects. The following parameter turned out as the most promising: The two paths described by the heart vector during QRS complex and later T-wave may be interpreted as loops in a 3D space. Connecting the two furthest points on each loop will provide two vectors including an angle. Referring to the authors the value of this angle is related to the risk of interest [204].

In year 2000, Okin et al. compared two criteria for the susceptibility to ventricular arrhythmia: the commonly used QT-dispersion and the relations of the first principal components of PCA applied on the reconstructed T-wave vector loop. The latter is described as superior, since it is more robust against fluctuations of T-wave offset markers [205]. It provides a measure for the quality of ventricular repolarisation.

A similar approach was proposed by M. Kesek et al. [206]. They employed PCA to divide the dipolar portion of the T-wave loop from the rest. The second is used to characterize the excitation propagation.

## ECG Signal Preconditioning

## 7.1 ECG Signal Low-Frequency Filtering

## 7.1.1 Motivation

The frequency of the baseline wander, as stated before, is usually in a range below 0.1 Hz in rest ECG and 0.65 Hz during stress test. Therefore, its presence will be reflected in the higher level DWT approximation coefficients. This is actually the basic phenomenon behind this approach aiming to eliminate the distortion of baseline wander in measured ECG signals. This elimination is accomplished by decomposing the noisy ECG signal, contaminated with baseline wander into a certain number of levels n using Discrete Wavelet Transform (DWT). The highest level , i.e. the n th level, approximation coefficients (AC) are supposed to represent the low frequency baseline variation signal. In the filtering algorithm proposed here, the n th level AC are set to zeros. Finally, the ECG signal is reconstructed following the same procedure as mentioned in section 4.1.7.

When a mother wavelet, e.g. coifflet 4, is arbitrarily chosen and DWT decomposition is carried out on one ECG signal with a sample frequency equal to 1 kHz, it was noticed that each of the 8 th , 9 th and 10 th level approximation coefficients, when time-aligned to the original ECG, resemble the baseline wander. Figure 7.1 shows this resemblance.

It is not very clear, as we see from figure 7.1, which level approximation coefficients represent the baseline wander signal the best in general. However, the following two issues need to be further investigated:

1. Which mother wavelet should be applied for DWT analysis on the noisy ECG to achieve the best results?
2. What value of n should be chosen? In other words, up to which level the ECG signal needs to be decomposed?

In order to answer these two questions, the following simulation is carried out.

## 7.1.2 Simulation

Before dealing with real ECGs, artificial signals were chosen for experimentation. These artificial signals are in fact mixtures of artificial free-of-noise ECG signals and artificial baseline variation signals. Thus, with a clear knowledge of the component signals, the performance of filtering could be judged.

(a)

Figure 7.1. The 8 th , 9 th and 10 th level approximation coefficients for an ECG signal with a sample frequency equal to 1 kHz and using Symlet4 as mother wavelet: (a) the ECG signal (b) the 8 th level approximation coefficients (c) the 9 th level approximation coefficients (d) the 10 th level approximation coefficients

<!-- image -->

.

Artificial noise-free ECG beats were generated by means of the algorithm used to generate noise-free ECG for Savitzky-Golay filter simulator and filter in Matlab Environment ((Signal Processing Toolbox)). Figure 7.2 shows an example of the generated noise-free ECG .

The sampling frequency was assumed to be 1 kHz, or in other words the span of 1000 samples is 1 second. The data length was taken to be 25000 samples, i.e. 25 seconds. In this case each beat should have a span of 1000 samples for 60 bpm (beats per minute) ECG and hence there would be 25 beats in total. For different bpm, the span of ECG beat was varied accordingly and hence the total number of ECG beats. To find out the suitable mother wavelet and the decomposition level n , tests were carried out on 650 artificially generated noisy ECG signals. Thirteen noise-free ECG signals in the range of 60 to 180 bpm (increment step value of 10 bpm) were created as discussed above. At the same time, a set of fifty sinusoidal signals with frequencies ranging from 0.01-0.5 Hz (with increment step value of 0.01 Hz) were created in order to simulate the baseline wander. Thereafter, as result, 650 test signals in total were synthesized by mixing the artificial ECG signals with artificial baseline wander signals in one to one correspondence.

Now, on each of the 650 test signals, the mixture signals, DWT analysis was carried out taking a total of 29 mother wavelets under consideration, i.e. symlet1, symlet2, ... symlet12, coiflet1, coiflet2, ... coiflet5, Daubechies1 (Haar), Daubechies2, ..., Daubechies12. By applying DWT decomposition a symmetric boundary value replication of the signal under decomposition in each level is employed during the convolution with analysis filters

Figure 7.2. An example of the noise-free ECG generated by Savitzky-Golay filter simulator in Matlab environment. The sample frequency is 1kHz and the heart rate is 120 beats per minute

<!-- image -->

or synthesis filters in order to deal with border distortions. The extension is done on both sides with the length of the half of the low-pass filter or high-pass filter.

On every test signal, for each of the mother wavelets, the following procedure was adopted.

1. Initialise n=1; i.e. no. of decomposition levels for DWT.
2. Decompose the test signal till n levels (maximal n here is chosen equal to 12) and get the DWT coefficients A n , D n , D n -1 , D n -2 ,..., D 1 , where A i = ith level approximation coefficients and D i = ith level details coefficients.
3. Perform the following two reconstructions:
- First Reconstruction : With A n to be all zeros, reconstruct the signal as in Figure 4.11. The signal, reconstructed in this way is called the ECG reconstruction . It should resemble the original noise-free ECG (with which the test signal is synthesized) for higher values of n.
- Second Reconstruction : Set all the coefficients other than A n (i.e. the details coefficients, D n , ..., D 1 ) to zeros, reconstruct the signal as depicted in Figure 4.11. The signal, reconstructed in this way is called the Baseline Reconstruction . It should resemble the original baseline variation signal (with which the test signal is synthesized) for higher values of n .
4. Judge the resemblance between the original and reconstructed signals by means of correlation. Two correlation coefficients ( CE &amp; CB ) were calculated, where CE is the percentage result correlation between the original noise-free ECG and the ECG reconstruction , or First Reconstruction and CB =correlation between original baseline variation signal (low frequency sinusoid) and the 'baseline Reconstruction'.
5. Repeat steps 2 to 4 for n = 1 , . . . , 12.

Furthermore, the whole above-mentioned process from step 1 to 5 was repeated for 29 different mother wavelets applied on the same test signal. Finally, for each test signal, two matrices were constructed, the first one includes all CE values and the other one includes all CB values. Each matrix is of size 12 × 29 and has the structure illustrated in figure 7.3.

Figure 7.3. The structure of each matrix derived from the baseline simulation process: C denotes either CE or CB . The 1 st to 12 th column represents Symlet Wavelets of 1st to 12th order (sym1, sym2, ... sym12), the 13 th to 17 th column represents Coiflet Wavelets of 1 st to 5 th order (coif1, coif2, ... coif5) and the remaining 18 th to 12 th column represents Daubechies Wavelets of 1 st to 12 th order (db1, db2, ..., db12).

<!-- image -->

For 650 test signals, there were 1300 correlation matrices in total, half for CEs and half for CBs . In addition two more matrices were computed, the first one is denoted as CE mean and represents the mean matrix of the 650 CE matrices, whereas the second one is denoted as CB mean and represents the mean matrix of the 650 CB matrices

## 7.1.3 Simulation Result

At this stage, the positions of the first L greatest elements in both matrices, CE mean and CE mean , were identified. The value of L was taken in this case equal to five, L = 5, because only the five greatest values in both matrices were greater than 99.99% . The positions are found to be exactly the same in both matrices, that is, the highest element occurs in the same position (same row and column number) in both matrices . The same is also true for 2 nd highest and so on. All of these five highest elements are found at the row corresponding to n = 9.

## 7.1.4 Discussion

From the simulation result, the baseline wander signal can be located perfectly at the 9 th level approximation coefficients of Daubechies11 mother wavelet from a baseline-wanderdistorted ECG signal sampled at 1000 Hz. Depending on subband theory in DWT, the 9 th level approximation coefficients of a signal sampled at 1000 Hz represents the signal in the [0-0.9766] Hz range. Therefore, some adaptation procedures are required for the system

Table 7.1. Results obtained from the baseline simulation done on 650 artificial test signals

|   Order No. | Mother Wavelet   |   n |   mean CE % | mean CB %   |
|-------------|------------------|-----|-------------|-------------|
|           1 | db11             |   9 |     99.9924 | 99.9150%    |
|           2 | sym12            |   9 |     99.9913 | 99.9011%    |
|           3 | sym10            |   9 |     99.9909 | 99.8962%    |
|           4 | db10             |   9 |     99.9906 | 99.8925%    |
|           5 | coif5            |   9 |     99.9904 | 99.8894%    |

to be able to handle equivalently ECG signals with different sampling frequencies. One of these procedures is simply to resample the signal under study to 1000 Hz. This procedure is actually a time-demanding solution, especially in the case of multi-channel ECG or long-time ECG. The second possible solution is to calculate the frequency band for all possible approximation coefficients decomposition levels of Daubechies11 mother wavelet, and then choose the frequency band nearest to the one obtained with our simulation, namely the [0-0.9766] Hz range. The corresponding decomposition level to that chosen band is indeed the level whose approximation coefficients need to be canceled.

This method is able to eliminate the baseline drift without any distortion of ST segment (see figure 7.5) as observed with conventional high pass filters, namely the second order Butterworth filter with 0.5 Hz cut off frequency (see figure 7.4). Moreover, it can be applied equally well to short and long duration ECG signals. The conventional filtered ECG showed only around 97% similarity to the noise-free ECG, whereas our waveletbased technique showed a similarity greater than 99.9%.

## 7.1.5 Proposed Method

In order to reach a high elimination of the baseline wander artifact in a corrupted ECG signal and to ensure least distortion in the ECG waveform, the results from the alreadyillustrated simulation are used to propose the following procedure:

1. Choose Daubechies11 as a first-best-choice mother wavelet (see the table 7.1).
2. Calculate the level of decomposition n , whose approximation coefficients need to be canceled. n is equal to nine when the sample frequency is equal to 1kHz, otherwise the method illustrated in the last section need to be implemented to calculate n .
3. Carry out DWT decomposition on the noisy ECG under study till the n th level.
4. Set the n th level approximation coefficients to zeros.
5. Reconstruct the ECG back using Inverse Discrete Wavelet Transformation (IDWT).

## 7.1.6 Results of Application on Real ECG

Our algorithm was applied on Multi-Channel ECG data recorded at our institute, as well as on signals taken from MIT- Arrhythmia Database. Figures 7.6 and 7.7 demonstrate the success of our method.

After eliminating the low frequency baseline wander, the next stage is filtering of high frequency disturbance in ECG.

Figure 7.4. The influence of using the conventional high-pass filter to remove the baseline wander on the ECG morphology and ST segment: In blue: the original noise-free ECG signal sampled at 1kHz and added to artificial 0.1 Hz baseline wander sin signal. In red: the filtered ECG obtained using the second order Butterworth filter with 0.5 Hz cut off frequency. The similarity (percentage correlation coefficients) between the noise-free and the filtered ECG signals is equal to 96.9 % and a large distortion in ST segment and the ECG morphology is noticed.

<!-- image -->

## 7.2 ECG Signal Denoising

## 7.2.1 Single-Channel ECG Denoising

## 7.2.1.1 Motivation

By analysing the approximation and details coefficients after applying DWT or SWT on any noisy ECG, it has been seen that the coefficients of the signal are confined to coarser scales, while those of the noise are observed in finer scales. In this case, denoising can be viewed as a nonlinear filtering operation in which the pattern of detail coefficients is exploited in order to produce a smoother signal. This operation involves three main steps, namely, calculating the SWT for the noisy signal, zeroing or modifying certain coefficients by a suitable rule, and reconstructing the signal from the modified coefficients.

Linear time-variant and linear time-invariant filtering has a limitation with noisy signals having fast changes. This limitation is that noise reduction can only be achieved at the price of considerable smoothing of the fast changes. On the other hand, the detail coefficients of the SWT can be subjected to nonlinear processing so that denoising is achieved without having to sacrifice too much of the fast changes in the signal.

Nonlinear techniques remove coefficients of the SWT below a certain threshold. The inverse SWT of the thresholded coefficients is then performed to produce a denoised signal. Suppose that CD are the details coefficients, denoising is achieved by hard thresholding on CD . This is defined by

Figure 7.5. In blue: the original noise-free ECG signal sampled at 1kHz and added to artificial 0.1 Hz baseline wander sin signal. In red: the filtered ECG obtained using our wavelet-based technique and canceling the 9 th level approximation coefficients of Daubechies11 mother wavelet. The similarity between the noise-free and the filtered ECG signals is equal to 99.991% and no distortion in ST segment or in the ECG morphology is noticed

<!-- image -->

(a)

Figure 7.6. Baseline cancellation result on record number 113, channel1, from MIT- Arrhythmia Database using our wavelet-based baseline filter: (a) the ECG signal corrupted with baseline wander artifact (b) the extracted baseline wander (c) the final filtered ECG signal

<!-- image -->

(a)

Figure 7.7. Baseline cancellation result on an arbitrary ECG segment from a recorded multi-channel signal using our wavelet-based baseline filter: (a) an ECG segment from a recorded multi-channel signal corrupted with baseline wander artifact (b) the extracted baseline wander (c) the final filtered ECG signal

<!-- image -->

<!-- formula-not-decoded -->

where ˜ CD is the filtered details coefficients CD and T r is the threshold. On the other hand, denoising by soft thresholding on CD is performed by thresholding the coefficients and shrinking them depending on the distance to the threshold T r [207],

<!-- formula-not-decoded -->

The threshold T r may be chosen as fixed, with a value based on some prior information that may exist on the signal. Under the assumption that the noise is white with variance σ 2 w , a fixed threshold T r , as derived in [147], is defined as:

<!-- formula-not-decoded -->

where the factor √ 2 ln N is the expected maximum value of a white noise sequence of length N and σ w is the standard deviation of the noise. Since σ w is unknown in practice, it is often estimated using the median of the absolute deviation,

˜ σ w = 1 . 483 .median ( CD ), (7.4) which avoids the influence of outliers values. The factor 1.483 is introduced to calibrate the median estimator with the standard deviation of a Gaussian PDF. In order to denoise

an ECG signal, a full SWT decomposition is applied first. Then, the global T r is calculated as illustrated in the equations 7.3 and 7.4 using only the first level details coefficient to estimate ˜ σ w of the noise, since this scale is the least influenced by the signal and most influenced by noise. The details coefficients of all levels will be afterward thresholded with the soft thresholding equation 7.2. The soft thresholding choice is the optimal one for any signal corrupted with white noise [155]. Finally, the final filtered ECG signal is obtained by performing ISWT using the original approximation coefficients of the last level and the modified detail coefficients of all levels. By applying SWT decomposition periodic boundary value replication of the signal under decomposition in each level is employed during the convolution with analysis filters or synthesis filters in order to deal with border distortions. The extension is done on both sides with the length of the half of the low-pass filter or high-pass filter at that level. In order to find the optimal mother wavelet to be used for SWT and ISWT in this ECG denoising method, the simulation presented in the following section was carried out.

## 7.2.1.2 Simulation

Thirty one conventional noise-free simulated 12-lead ECG signals of 10 seconds duration were generated by the simulator phantom 320 EKG-Simulator from the company M¨ uller &amp; Sebastiani Elektronik GmbH , (ms-gmbh.de). The simulator was connected to the MAC 5000 Resting ECG System from GE Healthcare, (gehealthcare.com), in order to record the simulated signals and save them in a digital readable form. All signals were taken with 500 Hz sample rate. The signal acquisition was supported by the company nabios GmbH 1 . These signals represent various physiological and pathological ECGs. A total number of 31x12 ECG segments are derived forming a database with 372 ECGs. The next step was to generate white Gaussian noise of 15 different levels. Starting at a signalto-noise ratio (SNR) equal to 4, the SNR first increased by steps of 2 until an SNR of 24 (11 levels), then by steps of 4 until SNR = 40. The noise was added to every signal. Thereafter, all noise-free ECG segments have been mixed with the 15 noise signals in one to one correspondence, so that a final set of 15x372=5580 noisy ECG signals were obtained. A total number of 29 mother wavelets, i.e. Daubechies1 (Haar), Daubechies2, ..., Daubechies12, coiflet1, coiflet2, ... coiflet5,symlet1, symlet2, ... ,symlet12, were taken under consideration for the simulation. The aim of this simulation is to find the best mother wavelet for the ECG denoising method presented above. The simulation steps are presented as follows:

1. A mother wavelet was first chosen.
2. A full SWT decomposition is applied on one of the final noisy signal.
3. The global T r is calculated as illustrated in the equations 7.3 and 7.4 using the first level details coefficient only.
4. The details coefficients of all levels are thresholded with the soft thresholding technique, equation 7.2.

1 nabios GmbH (Munich, Germany) is an internationally operating ECG core lab providing ECG processing and evaluation services to pharmaceutical companies.

5. The final filtered ECG signal is obtained by performing ISWT using the original approximation coefficients of the last level and the modified detail coefficients of all levels.
6. The similarity between the filtered ECG signal obtained in the last step and its corresponding original noise-free ECG, before the noise was added to it, is determined. This similarity was measured as the percentage result of the correlation coefficients between both signals.
7. The steps 3 to 6 were repeated for all noisy ECG signals.
8. The mean value of all similarity results for all noisy ECG signal and the mother wavelet chosen in step 1 was calculated.
9. The steps 2 to 8 were repeated for all mother wavelets under study.

## 7.2.1.3 Simulation Results

The optimal mother wavelet to be implemented in our wavelet-based denoising technique is chosen corresponding to the mother wavelet having the highest similarity result. The table 7.2 shows the best ten mother wavelet with their highest similarity results from the simulation. In a stem plot, figure 7.8 shows also the similarity results for all mother wavelets employed.

Table 7.2. Results obtained from the wavelet-based denoising simulation done on 5580 artificial test noisy ECGs and having values greater than 99% similarity

|   Order | Mother Wavelet   | Percentag   |   Similarity Result % |
|---------|------------------|-------------|-----------------------|
|       1 | symlet2          |             |                99.092 |
|       2 | daubechies2      |             |                99.091 |
|       3 | symlet4          |             |                99.066 |
|       4 | coiflet1         |             |                99.052 |
|       5 | coiflet2         |             |                99.05  |
|       6 | symlet6          |             |                99.023 |
|       7 | symlet5          |             |                99.012 |
|       8 | symlet1          |             |                99.007 |
|       9 | Haar             |             |                99.007 |
|      10 | symlet7          |             |                99.002 |

Figure 7.8 illustrates the result of applying our wavelet-method illustrated above with the best mother wavelet found, Symlet2, on a real ECG signal taken from one research study of Pfizer LTD .

## 7.2.1.4 Multi-Channel ECG Denoising

As mentioned in section 4.8.1.1, a new method was developed to filter the noisy 64channel ECG signal recorded with the SynAmps system. The method is based on improving the common-mode rejection ratio (CMRR) for the multichannel ECG measurement mathematically by changing the reference point on the right iliac fossa to Wilson Central

Figure 7.8. The percentage similarity results for all mother wavelets employed in the denoising simulation.

<!-- image -->

Figure 7.9. The result of applying our wavelet-method with coiflet2 on a real ECG signal taken from one research study of Pfizer LTD : In red, the original measured ECG signal. In blue, the filtered ECG signal

<!-- image -->

Terminal (WCT). In our measurements, ECG signal of a channel is actually the differential potential between the corresponding electrode of that channel and the reference electrode on the right iliac fossa. Recalling equation 3.5 and figure 4.21, the equation 3.5 can be re-written as follows:

<!-- formula-not-decoded -->

where φ A 13 , φ C 13 and φ C 24 are the potential of the right arm, left arm and left leg respectively referring to the ground electrode GN, see figure 4.21. In order to calculate the new ECG signals referring to WCT, we start to present the equation of ECG signals referring to the reference electrode RF as follows:

<!-- formula-not-decoded -->

where V n is the measured n th -ECG signal from the electrode n , φ n is the potential of the electrode n referring to the ground and φ RF is the potential of the reference electrode RF referring to the ground, see figure 4.21.

From equation 7.5 and equation 7.6, we can write,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

After arranging equation 7.8, the differential potential between the electrode n and WCT, V n wct , can be calculated as follows:

<!-- formula-not-decoded -->

From the equation 7.9, it can be noticed that the new ECG signal at the electrode n can be derived by subtracting the average signal between A13, C13 and C24 from the measured ECG signal at the electrode n . By performing this subtraction, the common-mode rejection ratio (CMRR) for the new ECG signals will be much improved compared to the measured ECGs. Figure 7.10 shows the improvement of the common-mode rejection ratio (CMRR) for the new ECG signal ( 7.10 -b) compared to the measured one ( 7.10a).

## 7.3 ECG Noise Estimation

## 7.3.1 Introduction

A robust low- and high-frequency noise estimation method in ECG signals will be presented in this section. As illustrated already, low-frequency noise in ECG signals is represented in the baseline wander signal and the high-frequency noise is defined as the highfrequency interference, the power-line interference (50/60 Hz) or the moving artefacts in the ECG signal. The noise estimation will be applied to know the overall indication of the ECG signal quality or to annotate the noise level in runs of beats or intervals.

Figure 7.10. The improvement of the common-mode rejection ratio (CMRR) for the new ECG signal (b) referring to WCT compared to the measured one (a) with the SynAmps system

<!-- image -->

## 7.3.2 ECG Low-Frequency Estimation

The level of low-frequency noise in an ECG signal can be estimated by canceling the baseline wander in the signal using the method presented in section 7.1 and comparing the similarity between the original signal x and filtered signal y by means of correlation coefficients technique. Finally, the ECG Low-Frequency Noise Estimation ELFE will be calculated as follows:

<!-- formula-not-decoded -->

where N is the number of samples of the original signal x and the filtered signal y , ¯ x and ¯ y are the sample means of x and y respectively, and finally σ x and σ y are the standard deviation of x and y , respectively.

## 7.3.3 ECG High-Frequency Estimation

The high-frequency noise in an ECG signal can be estimated by filtering the signal using the method presented in section 7.2.1 and using 'Symlet2' as mother wavelet, derive the noise signal, and finally calculate the root mean square (RMS) of the original signal x and the noise signal z . The High-Frequency Noise Estimation EHFE will be calculated then as follows:

where x i and z i are the i th sample in the original signal and the noise signal, respectively. The high-frequency noise estimation is a measure that represents how large the noise signal is in relation to bio-signal, which is ECG signal in this case.

## 7.3.4 Applications

## 7.3.4.1 Provide Quality Measure for Long-Time ECG Signals

The first use of the ECG noise estimation is to provide a quality measure for long-time ECG signals, i.e. Holter ECG tapes. The noise estimation will be able in this case to detect the runs of beats or intervals in the long-time ECG, where the signal includes high level of distortions due to high- or low-frequency noise. Detecting and annotating these segments will enable us to exclude them from any further analysis, like fiducial points detection, etc...

Excluding these segments will also reduce the processing and computation time on noisy tapes and will ensure high confidence level to the further process. ECG noise estimation on multi-channel long-time ECG signals will help also to provide a quality measure for each channel and therefore choose the best of them for the further analysis.

Figure 7.11 illustrates an original 30-minute ECG segment in red from the first channel of a 2-channel long-time ECG tape. The signal in blue is the filtered segment of the original red one after canceling the baseline wander effect and the electrode offset. In figure 7.11, three sbusegments, A, B and C are noticed. The subsegment 'A' represents the part of the original signal where there is no ECG signal. The 'no ECG' segments can be due to an off status in the Holter device or to an off status in the electrode from the chest of the patient, known as 'electrode-off'. The subsegment 'B' represents the calibration signal from the Holter with some small electrode-off parts. Whereas, segment 'C' represents the useful readable ECG signal. Figure 7.13 shows the baseline wander estimation of a 2-hour ECG signal whose first quarter is shown in figure 7.11. Each ELFE value is calculated from

<!-- formula-not-decoded -->

a window of 1000 samples from the original signal. In figure 7.13, the baseline wander distortion, i.e. ELFE values, in the subsegment 'A' and a small part of 'B' is very high. Whereas the baseline wander distortion in the subsegment 'C' is variable. Depending on the application and on the confidence of the further analysis, a threshold can be defined to accept all ECG segments, whose ELFE values are below it and reject the other ECG segments, whose ELFE values are above it, see figure 7.13. The threshold Threshold , provided in this example, is calculated as follows:

<!-- formula-not-decoded -->

where, mean ( ELFE ) and std ( ELFE ) are the mean value and the standard deviation of the ELFE vector.

Furthermore, the threshold could be set manually or automatically and depending on the further applications and the intended level of the confidence.

Figure 7.11. Baseline wander cancellation in a real 30-minute ECG segments from the first channel of a 2-channel long-time ECG tape. The original signal is in red, whereas the filtered one is shown in blue.

<!-- image -->

Figure 7.13 illustrates the high-frequency noise elimination in the ECG signal filtered from the effect of baseline wander illustrated in figure 7.11. In figure 7.13, the noisy ECG signal is plotted in red, whereas the clean one is plotted in blue. Furthermore, the three subsegments, 'A', 'B' and 'C', shown in figure 7.11, are still mentioned here as well. Figure 7.14-a, 7.14-b and 7.14-c illustrate a zooming out of the high-frequency noise elimination result in the three subsegments, 'A', 'B' and 'C', shown in figure 7.13, respectively.

Figure 7.15 shows the high-frequency noise estimation of a 2-hour ECG signal whose first quarter is shown in figure 7.13. Each EHFE value is calculated from a window of

Figure 7.12. The baseline wander estimation signal ELFE of the ECG signal shown in figure 7.11. The threshold is calculated with equation 7.12.

<!-- image -->

1000 samples from the original signal. In figure 7.13, the high-frequency noise distortion, i.e. EHFE values, in the subsegment 'A' and a small part of 'B' is very high, since the energy of high-frequency noise components are very high in these subsegments compared to the energy of the original signal. Whereas the high-frequency noise distortion in the subsegment 'C' is variable. Depending also on the application and on the confidence of the further analysis, a threshold can be defined to accept all ECG segments, whose EHFE values are below it and reject the other ECG segments, whose EHFE values are above it, see figure 7.15. The threshold Threshold , provided in this example, is calculated as follows:

<!-- formula-not-decoded -->

where, mean ( EHFE ) and std ( EHFE ) are the mean value and the standard deviation of the EHFE vector.

As in case of low-frequency noise estimation, also here, the threshold could be set manually or automatically and depending on the further applications and the level of the confidence.

## 7.3.4.2 Provide Quality Measure for Huge Databases of Short-Time ECG Signals

Electrocardiogram core laboratory, abbreviated as 'ECG core lab', provides expert, objective and accurate review of pre-specified, study-related ECG variables. An ECG core lab also processes a large number of ECG signals centrally to guarantee a systematic and high quality evaluation of the electrocardiograms. For a proper evaluation of electrocardiograms, a high signal quality of the recordings is essential. One responsibility of the ECG

Figure 7.13. the high-frequency noise elimination in the ECG signal filtered from the effect of baseline wander illustrated in figure 7.11.

<!-- image -->

core lab is to provide the ECG recording units (in general specialized 'Phase I' clinics or hospitals) with a feedback of their ability to record ECG signals. Therefore, the quality of ECG signals needs to be assessed accurately and retrospectively. Furthermore, it needs to be monitored during or after a certain study. Each study usually includes a huge number of short-time ECG signals. The company nabios GmbH has implemented the methods developed by the author of this thesis and described in section 7.3.2 and in section 7.3.3 to assess the effect of baseline wander distortion and the high-frequency noise in the study-related short-time ECG signals, respectively. After applying these noise estimating methods, an accurate overall quality assessment and a retrospective noise evaluation feedback can be obtained. Figure 7.16 illustrates the result of a retrospective baseline wander analysis on 1246 ECG signals from a Phase I study done by nabios GmbH using the algorithm provided in section 7.3.2. The respective correlation coefficient between the original signal and the baseline corrected signal for each tracing was obtained. Figure 7.16 displays a two-dimensional landscape of the ordered baselines (highest correlation coefficient first, lowest correlation coefficient, last). As can be seen the landscape evolves from flat lines (no baseline wander) to large baseline wander in the background.

## 7.4 ECG Delineation

## 7.4.1 Motivation

The first level details coefficients obtained from the Haar wavelet-based SWT decomposition of ECG signal are analysed in our method. In this section, we will try to discover the utility of Haar wavelet in ECG delineation. As depicted already in figure 5.7, Haar

Figure 7.14. High-frequency noise elimination result in the three subsegments, 'A', 'B' and 'C', shown in figure 7.13. a) zooming out of the high-frequency noise elimination result in the subsegment 'A'. b) zooming out of the high-frequency noise elimination result in the subsegment 'B'. c) zooming out of the high-frequency noise elimination result in the subsegment 'C'.

<!-- image -->

function has a step nature. This is found to be very sensitive to any slope change in the original signal. Before going to the real ECG signal, the Haar wavelet is applied on some signals with specific clear shape (e.g. a straight line with a constant slope, a triangular wave, a cosine wave etc). Every signal is decomposed into first level approximation A 1 and

Figure 7.15. The high-frequency noise estimation of a 2-hour ECG signal whose first quarter is shown in figure 7.13. Each EHFE value is calculated from a window of 1000 samples from the original signal.

<!-- image -->

Figure 7.16. The result of a retrospective baseline wander analysis on 1246 ECG signals from a Phase I study done by nabios GmbH using the algorithm provided in section 7.3.2.

<!-- image -->

details coefficient D 1 . The reconstruction is performed with A 1 set to all zeros. The signal, which is reconstructed back with setting A 1 all to zeros, is referred to as the First Level Details Signal (FLDS) throughout this chapter. Figure 7.17 shows the FLDS obtained from a straight line signal with constant slope, where all FLDS samples are noticed to be of the same amplitude and of alternating signs.

(a)

Figure 7.17. The First Level Details Signal (FLDS) obtained from a straight line signal with constant slope: (a) the straight line signal (b) the corresponding First Level Details Signal (FLDS). The samples of FLDS are of the same amplitude and of alternating signs.

<!-- image -->

In the same manner, figure 7.18 shows FLDS calculated from a symmetric triangular wave. It illustrates the following points:

1. Samples of FLDS are of the same amplitude and alternating signs as long as the slope remains constant.
2. When the slope of the signal is zero, FLDS samples have zero magnitude.
3. When there is a direction change, or sign change in slope, in the original signal, e.g. at the peak of a triangle, two consecutive samples of FLDS are of same sign. Here, when the slope changes its sign from positive to negative (i.e. direction of signal changing from +ve to -ve signifying a positive peak), this reflects two consecutive positive samples in FLDS, where the first one is marking the instant of direction change (or in other words, occurrence of peak).
4. The slope magnitude is the same on either side of the triangle, only the sign is different. This owes to the symmetry of the triangle. So, all the samples of FLDS falling under the span of the triangle are of same absolute magnitude.

It can be seen also that when there is a negative peak (signifying direction change of the signal from negative to positive sign), two consecutive samples in FLDS with negative sign can be detected. The first sample marks the instant of that peak, see figure 7.19. The following two characteristics are computed from the FLDS, on the basis of observations made so far:

1. Direction Change Mark (DCM) : This is a time vector comprising the same number of elements as the original signal or FLDS. All elements of this vector will have zero magnitude except at the direction changing points. Whenever there are two positive consecutive samples in FLDS, the element of DCM corresponding to the first sample will be '+1'. On the other hand, two consecutive negative samples of FLDS will reflect

(a)

Figure 7.18. The First Level Details Signal (FLDS) obtained from a symmetric triangular pulse: (a) the symmetric positive triangular pulse (b) The corresponding samples of First Level Details Signal FLDS. The two consecutive positive samples in FLDS mark the instant of direction change.

<!-- image -->

Figure 7.19. The First Level Details Signal (FLDS) obtained from a symmetric triangular pulse: (a) the symmetric positive triangular pulse (b) The corresponding samples of First Level Details Signal FLDS. The two consecutive negative samples in FLDS mark the instant of direction change.

<!-- image -->

- a '-1' in the corresponding element of DCM. Therefore, a '+1' in DCM will signify a positive peak in the original signal and a '-1' will represent a negative peak.
2. Direction Change Sharpness (DCM) : This is also a time vector having exactly the same span as DCM. All the elements of DCS will be zero except at those positions where DCM has a non-zero value. If DCM has a '+1', the corresponding sample of FLDS is tracked. The absolute difference in magnitude between this sample and the next sample of FLDS is calculated and this value is put at the corresponding position of DCS. If DCM has a '-1', again the corresponding sample of FLDS is tracked. The

absolute difference in magnitude between this sample and the next sample of FLDS is calculated like before. Now, this difference is multiplied with -1 and the resulting negative value is put at the corresponding position of DCS. Therefore, the samples of DCS will be a replica of those of DCM as far as the sign is concerned.

- If the DCM sample is zero, corresponding DCS sample will also be zero.
- If the DCM sample is positive (i.e. +1) , the corresponding DCS sample will also be positive (but can have any magnitude depending on FLDS).
- If the DCM sample is negative (i.e. -1) , the corresponding DCS sample will also be negative (but can have any magnitude depending on FLDS).

The next step is to see how the values of FLDS, DCM and DCS change corresponding to the signal under study. Therefore, a cosine signal will be presented as an example, figure 7.20. The slope of the cosine signal varies continuously and obviously the samples of FLDS follows the pattern of slope change closely. We have a collection of ordered pairs of consecutive samples, that is, elements belonging to the same ordered pair will have the same magnitude but opposite sign. This leads to the symmetrical positive and negative halves of FLDS. Moreover, two consecutive samples of FLDS (belonging or not belonging to the same ordered pair) are always of opposite signs. The only exceptions are found at the local extrema or maxima of the original signal ( where the slope changes its sign). However, DCM is only sensitive to the change in 'sign' of slope (i.e. a direction change in the signal) while DCS provides the change in 'magnitude' of slope at every sample of DCM.

Figure 7.20. Deriving FLDS, DCM and DCS from a cosine signal : (a) the cosine signal (b) the corresponding FLDS (c) DCM showing three direction change points (d) the DCS, showing the steepness change of the corresponding DCM

<!-- image -->

In the same way, FLDS, DCM and DCS are derived for QRS complex signal, P wave and T wave. A QRS complex, shown in figure 7.21, has five direction changing points, namely, Q onset, Q peak, R peak, S peak and S offset (also called J point). Whereas,

either P wave or T wave has three direction changing points, two points representing the wave boundaries and one point localizing the apex or the peak. Figure 7.21 shows the ability of DCM to detect and localize all the direction changing points in the given QRS complex signal. Furthermore, DCS illustrates the corresponding steepness value for every DCM value. Similarly, figure 7.22 and figure 7.23 show the ability of DCM to detect and localize all the direction changing points along with their corresponding DCS steepness values in the given measured P wave and T wave respectively. The whole direction changing points for an ECG beat are called the fiducial points or the significant points of that beat. Figure 7.24 shows the fiducial points of one ECG cycle detected by DCM and DCS values.

Figure 7.21. Deriving FLDS, DCM and DCS from a QRS complex: (a) a QRS complex signal (b) the corresponding FLDS (c) DCM showing five direction change points, namely QRS complex onset, Q peak, R peak, S peak and QRS complex offset (d) the DCS, showing the steepness change of the corresponding five DCM values. In this example, the R peak has the highest steepness among the all points

<!-- image -->

## 7.4.2 Single Channel Delineation Strategy

A single channel ECG delineation strategy is developed and presented in this section. This delineator is able to detect all fiducial points of every beat in the single channel.

## 7.4.2.1 R Peak and QRS Complex Detection

All the R peaks from the ECG data are detected first, after proper conditioning. For this purpose, we take help of a running window of adaptive length. The procedure can be described step by step as follows:

(a)

Figure 7.22. Deriving FLDS, DCM and DCS from a real P wave: (a) a P wave signal (b) the corresponding FLDS (c) DCM showing three direction change points, namely P onset, P peak and P offset (d) the DCS, showing the steepness change of the corresponding three DCM values.

<!-- image -->

Figure 7.23. Deriving FLDS, DCM and DCS from a real T wave: (a) a P wave signal (b) the corresponding FLDS (c) DCM showing three direction change points, namely T onset, T peak and T offset (d) the DCS, showing the steepness change of the corresponding three DCM values.

<!-- image -->

Figure 7.24. Detecting the fiducial points of a real ECG cycle using DCM and DCS values: (a) a real ECG beat (b) the corresponding FLDS (c) DCM showing eleven direction change points (fiducial points) (d) the DCS, showing the steepness change of the corresponding eleven DCM values. The names of the fiducial points are defined as follows: 1 ≡ Pon, 2 ≡ Ppk, 3 ≡ Poff, 4 ≡ Qon , 5 ≡ Qpk, 6 ≡ Rpk, 7 ≡ Spk, 8 ≡ Soff, 9 ≡ Ton, 10 ≡ Tpk, 11 ≡ Toff

<!-- image -->

1. Window Length Selection : The R peak detection process uses an adaptive window length (WL) strategy in order to ensure high sensitivity for all QRS complex and R peaks in the ECG signal under study. The mean RR interval of all RR intervals already detected is taken care of while deciding on the window length (WL) for the whole data. The WL should satisfy the following two conditions:
- It should be less than the mean RR interval. This will prevent false negative detection (see section 7.4.5).
- It should be larger than half of the RR interval, to prevent false positive detection (see section 7.4.5).

After optimizing the QRS complex detection algorithm with many long-time ECG signals and with many multi-channel ECG signals, The best WL is found to be between 55% and 60% of the actual mean RR interval calculated.

2. Extending Data Length : The ECG data-length is extended at the end by a set of samples of zero amplitude spanning WL. Provided the ECG length is equal to L, the new length will be (L+WL). This is done so that even the last data sample can be analysed properly. The window translation is carried out the signal of length (L+WL). Translation is stopped when the remaining data length is found to be less than WL.
3. Running the Adaptive Length Window : The window is made to run over the whole data set ,spanning L+WL, in steps. A small incremental step (IS) will take longer computation time. However, a long incremental step might introduce errors in detection (the reason will be clear in the next section). The optimal incremental step (IS)

of ECG, sampled in the range of 250-1000Hz, is found to be between 5 msec and 20 msec. IS should be chosen in such a way that WL is always divisible by it. In order to explain the following steps effectively, we suppose that the morphology of the ECG under study is similar to the ECG morphology in lead II. The instant of occurrence of the max value of DCS inside each window is noted. If the window encompasses any R peak, then it will cause the sharpest direction change in the ECG, and hence the max value in the corresponding sample of DCS. The time of occurrence of the highest DCS value for each and every window will be accumulated in a vector called Extreme Direction Change Sharpness (EDCS). If the ECG channel contains negative R peaks, the time of occurrence of the lowest values of DCS will be accumulated in EDCS. Figure 7.25 shows an ECG channel consisting of positive R peaks. Hence, the instant of occurrence of the highest DCS value inside each window is saved in EDCS. Also it is seen that in each ECG beat, the DCS corresponding to the positive R peak is the highest. If the same R peak is enveloped by n consecutive windows, the same value will occur consecutively n times in the EDCS vector, see figure 7.25.

All windows enveloping and tracking the same R peak will reflect the same value in EDCS. Assuming that the first window enveloping this R peak in figure 7.25 is the i th running window, so the last window tracking the same R peak and giving the same EDCS value in this case will be the ( i + n -1) th running window. From the ( i + n ) th onwards, this R peak will not be encompassed. The end of the i th window and the start of the ( i + n ) th one are exactly coincident. This is ensured by the divisibility of WL by IS. Hence we can easily interpret that,

<!-- formula-not-decoded -->

4. Identification of R peaks from EDCS Value : when the elements in EDCS occur n times consecutively, the location of R peak will be detected as the last element (sample) of the first window covering the highest DCS value. For larger IS, the total number of window positions (in course of translation) will be smaller and that will lead to smaller accumulation of each individual R peak in EDCS. Under such circumstances, the accumulation of R peak might become comparable with that of P or T peaks. This is why IS should be kept as small as possible depending on the computation time that can be allowed and the memory resources. The mean RR interval obtained from the previous segments is taken care of to determine the window length WL for the next segment.
5. Enhancement of DCS : It is clear that the success of R peak localization solely depends on the elements of EDCS, which are in turn determined by the samples of DCS. If some mechanism can be devised which will enhance the DCS samples corresponding to R peak locations, that will surely be an improvement in our methodology. With this aim, three different sets of DCS are calculated:
1. DCS up : ECG signal (after extending by WL) is up-sampled by a factor of 2 and the DCS corresponding to this upsampled ECG is computed. Now, in order to achieve the same length (L+WL) as the normal ECG, this DCS is downsampled by 2.

Figure 7.25. Detecting R peak: a) a real ECG beat. d) the corresponding DCS signal.

<!-- image -->

2. DCS normal : The DCS obtained from the ECG signal (after extending by WL) with normal sampling rate.
3. DCS down : Original ECG Signal (after extending by WL) is down-sampled by a factor of 2 and the DCS corresponding to this down-sampled ECG is calculated. Now, in order to achieve the same length (L+WL) as the ECG, this DCS is upsampled by 2.

Therefore, all the three, namely, DCS up , DCS normal and DCS down are time aligned with the normal ECG signal (originally recorded). We calculate the modified DCS as follows,

<!-- formula-not-decoded -->

The window translation is carried out DCS modified . EDCS formation and thereafter R peak detection is now made considering the modified DCS. Up-sampling is done by means of interpolation and down-sampling, by discarding every alternate sample. Figure 7.26 shows the enhancement of DCS modified in comparison to DCS normal corresponding to R peak locations.

The vertical scales should be noted while comparing DCS normal and DCS modified in the above figure. This modified DCS is only used for R peak detection. For delineation of P,Q,S and T waves we use only DCS normal (referred to as DCS).

## 7.4.2.2 P &amp; Q Waves Detection

After detecting all R peaks in the ECG, we now zoom into each and every beat. A search window, spanning half of the previous RR interval is taken prior to each detected R peak.

(a)

Figure 7.26. Enhancement of R Peak and QRS complex detection: (a) ECG segment (b) the corresponding DCS signal (c) the corresponding modified DCS , DCS modified , using the equation 7.15. It is shown in DCS modified the improvement in amplitude of the DCS coefficients corresponding to the inverted R peaks in to the original signal (a).

<!-- image -->

Figure 7.27 shows an example of a positive R peak, negative Q peak and positive P peak, reflecting '+1', '-1' and '+1' in DCM respectively. The '-1' in DCM immediately prior to the R peak is the location of Q peak. The '+1' just before the Q peak is the onset of Q wave. Had the Q peak been positive, it would have caused a '+1' in DCM and the corresponding Q-onset a '-1'.

Now after detecting the Q onset, the highest positive DCS value prior to it is located. This is the P peak. The two '-1' in DCM surrounding the P peak are its onsets and offsets. Had the P wave been negative, search should have been made for the lowest negative DCS value to locate the peak and the two surrounding '+1' in DCM for the onset and offset.

## 7.4.2.3 T &amp; S Waves Detection

In a similar method to P and Q waves detection, S and T waves are detected and delineated in each and every beat after detecting all the R peaks in the filtered ECG. Here, for each beat, a search window spanning half of the next RR interval is taken next to each detected R peak.

Figure 7.28 shows an example of positive R peak, negative S peak and positive T peak, causing '+1', ' -1' and '+1' in DCM respectively. The '-1' in DCM immediately next to the R peak is the location of S peak. The '+1' in DCM immediately after the S peak is the offset of S wave. Had the S peak been positive, it would have reflected a '+1' in DCM and the corresponding S-offset a '-1'. On the right of S offset, the T wave peak, onset and offset are determined in the same manner as it is for P wave.

Figure 7.27. Detection and delineation of P and Q waves: (a) ECG signal in a search window taken prior to the detected R peak, ending at R peak and and spanning half of the previous RR interval (b) the corresponding FLDS signal(c) the corresponding DCM signal(d) the corresponding DCS signal

<!-- image -->

Figure 7.28. Detection and delineation of T and S waves: (a) ECG signal in a search window taken after the detected R peak, starting at R peak and spanning half of the following RR interval (b) the corresponding FLDS signal(c) the corresponding DCM signal(d) the corresponding DCS signal

<!-- image -->

## 7.4.3 Multi-Channel ECG Delineation

When there are many different channel data pertaining to the same ECG record, it is reasonable to take into consideration the delineation results obtained from a number of channels to reach the final decision aiming to reduce the delineation errors. The delineation errors are mainly due to the high noise level and artifacts in the single-channel ECG under delineation process. The R peak detection is carried out simultaneously on several channels. The selected channels for this purpose should have a morphology similar to that illustrated in figure 7.24 -a, or in figure 7.26 -a. The number of the ECG channels having similar morphology according to our 64-channel ECG electrode set is round 25 channels. The multi-channel ECG delineation detection strategy will start with singlechannel ECG delineation for each individual channel as described before. Afterward, the final delineation results will be obtained by the means of a histogram-based method. That is, a histogram for the available detected results of a similar significant point in the ECG signal will be used to have the final overall position of that significant point. The same procedure will be done and repeated on all detected points available in the ECG signal under consideration. The general rule for choosing the final position is to find out the detected point with the highest frequency of occurrence value in the histogram. If more than one value is found to satisfy the same condition, the mean of them is taken as the final decision. In order to illustrate the last histogram-based criterion, the following example is considered. Supposing that 10 R peak results are detected in 10 channels for the same cardiac beat. A histogram plot of these values is given in figure 7.29.

Figure 7.29. A histogram plot of 10 R peak results detected in 10 channels for an ECG cycle

<!-- image -->

It is seen from the histogram in figure 7.29 that the values 100 and 99 are having the highest frequency of occurrence. Therefore, the final decision regarding this R peak

location will be the sample number, obtained as the integral mean of 100 and 99 ( i.e. 100).

The number of false positive or false negative detections (defined in section 7.4.5) can be reduced considering multiple channel results. In order to be accepted as a final decision, the same R peak needs to be detected at least in half the number of selected channels. This way, false positive detection is reduced. On the other hand, if there is any false negative detection in one channel, the same can be corrected considering delineation results from other channels. This way, our delineation algorithm becomes more robust and independent of single channel errors.

After computing the final decision regarding the R peak location in multi-channel ECG, next step is the delineation of P,Q,S and T waves. Again simultaneous detection is performed on selected number of channels. The channels selected for P/T wave delineation should have a prominent unipolar P/T wave (negative or positive peak). Channels selected for Q/S delineation should show prominent Q/S spikes. The same kind of histogram-based method is used to get the final delineation result for P peak, P onset, P offset, QRS onset, Q peak, S peak, J point, T onset, T peak and T offset. Each delineation stage is dependent of the previous stage. The channels for delineation should be selected judiciously so as to ensure prominent wave-shapes.

## 7.4.4 Multi-Channel ECG Delineation Results

Figure 7.30 shows a lead II heart cycle derived from a 64-channel ECG signal along with its corresponding delineation results computed by means of the multi-lead delineation approach, described in section 7.4.3. Figure 7.31 shows a heart cycle measured from a single channel of a 64-channel ECG signal along with its corresponding delineation results computed by means of the multi-lead delineation approach, described in section 7.4.3.

## 7.4.5 Single ECG Delineation Validation

The performance of the delineation algorithm, namely for R peak, was evaluated by comparing our automatic delineation results against manually annotated delineation results. That is, the algorithm of single-channel R peak detection was tested on several randomly chosen records taken from MIT-Arrhythmia database. The performance of the delineation algorithm was evaluated by comparing the output of our algorithm with the manual annotation provided with each record.

This comparison was done on the basis of the mean error ME and standard deviation SD between our and their annotations as well as the sensitivity Se and the positive predictivity P + of our result compared with the MIT reference.

ME along with SD represent together the delineation success of the automatic segmentation algorithm. High SD and ME values indicate high instability and low accuracy for the automatic delineator compared to the manual annotation and vice versa in case of low SD and ME values. ME and SD are usually calculated in msec .

The sensitivity Se and the positive predictivity P + are defined and calculated as follows:

<!-- formula-not-decoded -->

Figure 7.30. a lead II heart cycle derived from a 64-channel ECG signal along with its corresponding delineation results computed by means of the multi-lead delineation approach, described in section 7.4.3.

<!-- image -->

Figure 7.31. a heart cycle measured from a single channel of a 64-channel ECG signal along with its corresponding delineation results computed by means of the multi-lead delineation approach, described in section 7.4.3.

<!-- image -->

<!-- formula-not-decoded -->

where TP , TN and FP are the abbreviations of True Positive , True Negative and False Positive respectively.

If the automatic method is able to detect truly a point within a specified tolerance around its corresponding manual annotation, the TP counter will be increased by one. On the other hand, FP counter will be increased by one, when the automatic method is able to detect a point outside the mentioned specified tolerance around its corresponding manual annotation. In case of the inability for the automatic method to detect any point within or outside the corresponding manual annotation, FN counter will be increased by one.

Table 7.3. Validation of the single-channel delineation method, presented in section 7.4.2, on MIT-Arrhythmia database.

| Rec. No.   |   Ch. No. |   No. of Sample |   FN |   FP |   TP |     Se |    %P+ |   %ME msec |   SD msec |
|------------|-----------|-----------------|------|------|------|--------|--------|------------|-----------|
| '100'      |         1 |          650000 |    0 |    1 | 2271 | 100    |  99.96 |     -1.9   |      2.46 |
| '101'      |         1 |          650000 |    3 |    4 | 1863 |  99.84 |  99.78 |     -0.48  |      1.18 |
| '103'      |         1 |          650000 |    0 |    0 | 2084 | 100    | 100    |     -2.23  |      2.31 |
| '113'      |         1 |          650000 |    3 |    4 | 1791 |  99.83 |  99.78 |     -1.74  |      1.38 |
| '115'      |         1 |          650000 |    1 |    6 | 1953 |  99.95 |  99.69 |     -3.16  |      3.54 |
| '122'      |         1 |          650000 |    6 |    5 | 2469 |  99.75 |  99.8  |     -3.95  |      5.87 |
| '234'      |         1 |          650000 |   20 |    1 | 2732 |  99.27 |  99.96 |     -1.43  |      1.26 |
| '100'      |         2 |          650000 |    1 |    0 | 2271 |  99.95 | 100    |      0.736 |      2.4  |
| '103'      |         2 |          650000 |    0 |    0 | 1294 | 100    | 100    |     -2.97  |      3.08 |

Table 7.3 shows the validation of the single-channel delineation method, presented in section 7.4.2, on MIT-Arrhythmia database.

The overall sensitivity Se and the positive predictivity P + obtained for MIT-Arrhythmia database are found to be 99.84% and 99.89%, respectively. Furthermore, the overall mean error and standard deviation are -1.96175 msec and 2.7775 msec , respectively.

The overall sensitivity Se , obtained by [170] and [141], are found to be 99.89% and 99.88%, respectively. Whereas, the positive predictivity P +, obtained by [170], is found to be 99.94%. As noticed, these values are slightly higher than ours. However, as presented already, the result of Se and P + depends very much on the tolerance period taken when calculating TP , TN and FP . The value chosen in this analysis is ± 10 msec . The value in the literature is not explicitly given.

The overall mean error and standard deviation values, obtained by our method, show the best result among all other methods providing high stability and accuracy to our automatic R peak delineator. The detection of other important fiducial points using our delineator, like Q on and T off , needs to be carried out in the future.

## 7.4.6 Discussion and Conclusion

This method is based on the simplest Wavelet prototype and dealing only with the first level details coefficients allowing a relatively fast delineation process for multi-channel ECG. Furthermore, it provides an accurate detection for the significant points without using any kind of threshold techniques. Haar Discrete Wavelet transform and the

histogram-based technique used in this approach allow for perfect P, QRS and T detection and delineation either in multi-channel ECG data or even in single-channel ECG.

## 7.5 ECG-Complex and ECG-Wave Extraction

The aim of ECG-complex and ECG-wave extraction is to create the input data matrix for the further analysis with Principal Component Analysis (PCA). It is done through four main steps. For a better understanding, we suppose that the QRS complexes of a particular ECG single-channel need to be extracted into a matrix. The main steps are illustrated as follows:

1. Determining the longest QRS span : The QRS interval is defined as the time length between the Q wave onset until the S wave offset. The longest QRS span is determined and a safety factor is added to it in order to take care of errors in delineation. If this comes to be an even number, we make it odd by adding 1 to it.
2. Initialising the Signal Extraction Matrix (SEM) : This matrix should have as many number of rows as the number of detected beats in the corresponding ECG data set. The number of columns should be the longest QRS span, defined in the first step.
3. Positioning of R peak : Although the delineation is carried on the ECG after two stages of filtering, QRS complexes are extracted from the first-stage filtered ECG (i.e. only after canceling baseline wander but without high frequency filtering). R peaks detected by the delineator are copied to the middle column of SEM.
4. Copying the QRS complex : After positioning the R peak in the middle column of the respective row, the ECG sample magnitudes are copied from both sides of the R peak into SEM.

Figure 7.32 shows three extracted QRS complexes as an example from the final result obtained from extracting QRS complexes of a particular ECG single-channel. The same steps are followed in case of P waves or T waves extraction. In case of QRST complexes, the longest QRST complex span is first determined and the corresponding SEM Matrix will be then created. Afterward, QRST complexes are copied to SEM starting from their detected QRS complexes (Q onsets). Copying QRST complexes does start at the first column of SEM, but after some columns as safety factor. The value of the samples before and after the QRST complexes inside SEM are considered zeros.

## 7.6 Detecting Outliers in the Automatic ECG Segmentation

## 7.6.1 Introduction

One of the most important problems in ECG analysis is the accurate measurement and assessment of ECG intervals, waves and complexes. QT interval and its changes, for instance, give a clear indication for many abnormalities. Therefore, high level of accuracy should be associated with QT interval measurements to prevent false evaluation. In that regard, manual and automatic measurements are used. Manual measurement is very time-consuming, especially when analyzing long-term Holter ECGs. Moreover, it is

.

.

Figure 7.32. Three extracted QRS complexes (row vectors) as an example from the final Signal Extraction Matrix (SEM). Due to a possible delineation error, QRS complexes are not always perfectly aligned. However, the misalignment error is normally very small. In order to provide better explanation, the misalignment in this example is presented much larger than the real situation.

<!-- image -->

not immune to errors related to observer fatigue and lapses of attention. On the other hand, semi- or fully-automated methods offer advantages in terms of efficiency and cost considerations. However, no automated system can achieve the same level of accuracy as an expert ECG analyst [180]. In fact, unusual, ectopic and noisy ECG morphologies very often contribute so much effectively in producing many unreliable results in automated techniques. Therefore, an effective tool to eliminate wrong results will provide a high level of confidence and improve the performance of the whole automatic systems. Relatively little has been published on using confidence measures in ECG automatic segmentation system. One paper described the use of a Hidden Markov Model (HMM) in automated QT interval analysis as a confidence measure. They assess the confidence measure for an ECG waveform by considering both the log likelihood value for the waveform and its length. In order to determine the range of confidence measures for normal ECG waveforms, the Hidden Markov Model needs to be trained using 100 clean ECG waveforms measured

over a range of different heart rates. Thereafter, the confidence measure for each waveform in the data set will be evaluated [180]. In this section, a new and effective method for providing measures of confidence for automated ECG segmentation process will be presented [208]. It is based on Principal Component Analysis (PCA) and Hotellings T squared. As defined, Hotelling's T squared is actually a quantity indicating the overall conformance of an individual observation vector to its mean or an established standard [144]. In other words, it is a measure of the multivariate distance of each observation from the center of the data set [1]. Because the use of PCA and Hotellings T squared shows high efficiency, they are applied extensively in Statistical Process Control (SPC), finding outliers and measures of quality control [145].

## 7.6.2 Method

1. Construct a Mean-Subtracted Data Matrix B : The SEM matrix, obtained as described in section 7.5, will be used as an input matrix in this method. SEM matrix, denoted as SEM , is a training set with N samples (observations) and each sample SEM i can be expressed by a row vector with the size of M (dimensions) as follows:

<!-- formula-not-decoded -->

Thereafter, the empirical mean along each dimension m = 1... M is calculated. Afterward, all computed mean values are placed into an empirical mean row vector u of dimensions M .

<!-- formula-not-decoded -->

Afterwards, The empirical mean row vector u is subtracted from each row of the data matrix SEM . Then a new mean-subtracted data matrix B ( N × M ) is derived.

<!-- formula-not-decoded -->

where h is a column vector of ones and size of N x 1 : h ( n ) = 1 for n = 1 . . . N ,

2. Find the covariance matrix : The empirical covariance matrix C is calculated from the outer product of the zero-centered matrix B with itself:

<!-- formula-not-decoded -->

item Calculate the Eigenvalues and Eigenvectors of the Matrix C : The eigenvalue matrix D and the eigenvector matrix V of the covariance matrix C

<!-- formula-not-decoded -->

and the columns of the eigenvector matrix V and eigenvalue matrix D are sorted out in order of decreasing eigenvalues maintaining the correct pairings between the columns in each matrix.

3. Compute PCA Scores : The projected PCA-scores or the reconstruction parameter vectors (RPV) are the columns of the matrix Z ( N × M ), namely Z i 1 , Z i 2 , · · · , Z iM , where i = 1 ...N . The matrix Z is calculated by multiplying the eigenvector matrix with the zero-mean data matrix from the left as follows:

<!-- formula-not-decoded -->

The rows of Z correspond to the observations, whereas the columns refer to the components or dimensions.

4. Calculate Hotelling's T Squared Vector : Hotelling's T Squared Vector, denoted as T 2 , is a column vector of size ( M × 1). It is calculated as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where

The equation 7.25 is a weighted sum of all squared values of PCA scores (Reconstruction Parameter Vectors). Since all λ k are sorted with falling size, larger indices k are weighted stronger. Thus, deviations from mean are measured with stronger increasing values in case of larger deviations.

5. Set a Threshold for the Values of Hotellings T squared Vector : By setting a certain threshold, only the Hotellings T squared values lying below it along with their corresponding original row signal in SEM matrix will be kept as reliable results. The threshold could be set automatically or manually.

## 7.6.3 Results

This method has been tested on 60 normal and 10 TDP 24-hour two-channel recordings from different studies recorded during Dofetilide clinical trials (Pfizer, Inc.). Figure 7.33 shows an example of an 8000-QRS complex SEM matrix. It illustrates also that there is a number of outliers.

After calculating Hotelling's T square measure for every beat (QRS complex) of the SEM presented in figure 7.33 using the method presented in this section, a certain threshold is defined, (see figure 7.34). The threshold is calculated in this example by adding the mean value of Hotelling's T square vector mean ( T 2 ) to its standard deviation std ( T 2 ),

<!-- formula-not-decoded -->

Thereafter, only beats with Hotellings T squared values lying below the chosen threshold along with their corresponding original row signal in the 8000-QRS complex SEM matrix will be kept as reliable results, see figure 7.35.

Figure 7.33. 8000-QRS complex Signal Extracted Matrix (SEM). The matrix contains useful QRS complexes as well as a number of outliers.

<!-- image -->

## 7.6.4 Discussion and Conclusion

The method presented in this section is able to detect outliers and ectopic beats in a data set by comparing the morphology derivation of all input signals to their overall mean value in form of beat-to-beat analysis. Furthermore, it can be applied automatically or semi-automatically depending on the way of choosing the threshold and canceling the outliers. Furthermore, it produces reliable cancellation of unusual ECG segments without any need for a training or learning phase prior to application.

## 7.7 ECG-Complex and ECG-Wave Fine Alignment

If the delineation process is made perfectly, then the extracted signals will be perfectly time-aligned. However, if there is any small error in delineation result, it will lead to an undesirable misalignment. Hence, an improved alignment of the extracted useful signals needs to be performed. In other words, the aim of ECG-complex and ECG-wave alignment is to eliminate any small misalignment error before further analysis with PCA. Here, different variables mean different QRS complexes. The total no. of observations should be taken so that even the longest QRS interval is taken care of. A fine-alignment method, based on correlation technique, has been employed on the signals extracted into the SEM Matrix after removing the outliers. The procedure of this method is described as follows:

Figure 7.34. Hotelling's T square vector of the signal presented in figure 7.33. The threshold is calculated using the equation 7.26

<!-- image -->

1. Calculate the mean vector of all extracted signals by taking the mean of all rows of free-of-outliers SEM. This mean vector is considered as the template of the finealignment method. The idea of using the mean vector as a template for our method was adapted from [209, 210].
2. Calculate the correlation coefficient between each of the signal extracted and the template.
3. Shift each of the extracted signal by a number of steps (samples) toward left and toward right (+3 and -3 samples for example) from the template and go on calculating the correlation coefficient between the template and the signal at that position.
4. Each extracted signal is finally aligned at the position corresponding to the highest correlation coefficient. The final matrix containing aligned extracted signals is referred to as the PCA Input Matrix (PIM).

Before applying the alignment method described above on real extracted signals, its performance has been tested and validated. Hundred shifted Meyer wavelet scaling functions were generated and considered as testing input signals. Due to its morphology similarity with QRS complex, Meyer wavelet scaling function ϕ m was chosen for this testing purpose. It is defined in the frequency domain as follows:

<!-- formula-not-decoded -->

Figure 7.35. The result after applying the alignment algorithm on 8000 measured QRS complexes. It shows effective cancellation of outliers.

<!-- image -->

where

In order to generate the hundred shifted wavelet scaling functions, the lower and the upper border of the angular frequency | ω n | for the Meyer scaling function number n was chosen as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

For every Meyer wavelet scaling function, 1024 samples with sampling step δ equal to 16 π 3 1024 were chosen.

× Figure 7.36 shows the 1 st , the 50 th and the 100 th Meyer wavelet scaling functions and figure 7.37 illustrates the result after applying our alignment method on these hundred functions. The result shows 100% overlapping for all of the hundred signals.

Figure 7.38-a shows a real 60-beat misaligned QRST complexes from a single-channel ECG signal of a IBT 64-channel ECG databases from ActiveTwo system and 7.38-b shows the aligned complexes after applying our method.

Figure 7.36. The 1 st , the 50 th and the 100 th out of hundred shifted wavelet Meyer functions with 1024 samples each.

<!-- image -->

Figure 7.37. The result after applying the alignment algorithm on the hundred shifted wavelet Meyer functions. It shows 100% overlapping for all of the hundred signals.

<!-- image -->

Figure 7.38. Alignment of 60-beat QRST complexes from a single-channel ECG signal of an IBT 64-channel ECG databases from ActiveTwo system: a) The misaligned QRST complexes. b) The aligned QRST complexes

<!-- image -->

## T-Wave Morphology Analysis

## 8.1 Detecting Predisposition to 'Torsad de Points'

## 8.1.1 Introduction

In fact, cardiac safety is now a major issue in new drug development, because there is increasing awareness that many non-antiarrhythmic drugs can prolong the QT interval and provoke Torsade de Pointes (TDP) [117]. In particular the duration of the ventricular depolarization and repolarization has been identified as a surrogate marker for possible proarrhythmic effects of cardiovascular and non-cardiovascular agents. The European, the Canadian, and the American regulatory authorities have published independently 'guidance' documents for studies and evaluations of electrocardiograms targeted at the preclinical and clinical assessment of drug safety. All documents emphasize the importance of the analysis of possible QT interval prolonging effects.

Therefore, inevitably, QTc interval prolongation has come to be recognized as a surrogate marker of the risk of TDP. Although it is the best and the simplest clinical measure that is available at present, QTc interval is not a reliable surrogate of TDP. Intramyocardial dispersion of repolarization appears to play a more important role both in electrical stability of the ventricles and in arrhythmogenesis. Although the concept of QT dispersion is the best known and most widely investigated, it has also proved to be the least successful in predicting the risks of drug-induced TDP [211]. It is of major importance to mention again that the 'classical' concepts of QT dispersion do not determine the dispersion of repolarization times.

Monitor carefully the T wave morphology (TWM) changes in beat-to-beat manner appears to play a more important role in access the electrical stability of the ventricles and in detecting predisposition to TDP. Changes of T wave morphology are a much better measure of changes in repolarization times as compared to QT dispersion. That is, analysing the beat-to-beat changes and variability in TWM seems to be a robust precursor to TDP as seen in figure 8.1, where TWM variation are noticed clearly in a random segment of ECG signal taken round 6 hours before TDP episode.

In this chapter, Principal Component Analysis (PCA) was applied on T waves of 60 normal and 10 TDP two-channel tapes from different studies recorded during Dofetilide clinical trials (Pfizer, Inc.). PCA is the optimal linear technique which retains the maximum amount of variance within the projected feature spaces. PCA is employed to extract morphological features represented by its scores for T waves. The beat-to-beat fluctuation

Figure 8.1. T wave morphology variation in an ECG recorded round 6 hours before TDP episode

<!-- image -->

of the first PCA scores represents the deviation of T wave morphology. The first PCA scores, accounting for as much of the variability in the data as possible, are then analysed in order to assess the degree of variation for all T waves compared to their mean T wave, i.e. the beat-to-beat T-wave morphology variation throughout the whole channel. The procedure is presented in details in this chapter.

## 8.1.2 Methods

## 8.1.2.1 Data Preconditioning

First of all, the baseline wander correction method presented in section 7.1 is used to filter out the whole data set under studies, see figure 8.2.

The next step is to localize QRS complex onset, R peak and T wave offset for every beat in the whole 24-hour two-channel healthy and TDP tapes. The single-channel delineation method, presented in section 7.4.2, is employed, see figure 8.3.

In order to get rid of unusual, ectopic and noisy detected beats and outliers, the method described in section is used as an effective tool to eliminate the wrong results. It provides a high level of confidence in the data to be analysed further. Figures 8.4 and 8.5 show scatter plots between RR interval and QT interval of one healthy ECG and one TDP ECG respectively.

After localizing QRST complexes, free of outliers or ectopic beats, in each channel, QRST complexes belonging to the same channel are extracted and assembled in one matrix, so that they represent the rows of the matrix SEM (see section 7.5), see figure 8.6.

Afterward, each QRST complex in this matrix is shifted toward right and left a certain small number of samples and finally aligned at the position corresponding to the highest

Figure 8.2. The location and the orientation of the human heart in the chest [6]

<!-- image -->

Figure 8.3. Localizing QRS complex onset, R peak and T wave offset for every beat in the whole 24-hour two-channel healthy and TDP tapes.

<!-- image -->

correlation coefficient between this QRST complex and a chosen template signal, which is in this case the average of all QRST complexes. The aim of this fine alignment is to correct for any tiny misalignment between the extracted QRST complexes to their R peaks in order to provide a suitable input for the further analysis (see section 7.7), see figure 8.7.

Figure 8.4. A scatter plot between RR interval and QT interval of a healthy ECG with 80079 beats included.

<!-- image -->

Figure 8.5. A scatter plot between RR interval and QT interval of a TDP ECG

<!-- image -->

Thereafter, a low-pass second-order Butterworth filter with cut-off frequency of 20 Hz was applied on each QRST complex in the matrix, see figure 8.8 and figure 8.9.

The input matrix for the next step, denoted as T , is a submatrix of QRST-complex matrix. It has the same number of rows (signals), but it has smaller number of columns as it starts from a chosen common point on ST segments from the QRST complexes and

Figure 8.6. Extracted QRST complexes belonging to the same channel and assembled in one matrix

<!-- image -->

Figure 8.7. Aligned QRST complexes to their R peaks

<!-- image -->

has the same end of the bigger matrix covering and including only T waves, see figure 8.10.

## 8.1.2.2 Morphological Feature Extraction Using PCA

1. Organizing the data set : Suppose that the matrix T , plotted in figure 8.10, is a training set with N samples and each sample T i can be expressed by a row vector with the size of M as follows:

Figure 8.8. Original and its corresponding filtered T waves. In blue: the original signal. In red: the filtered signal after applying a low-pass second-order Butterworth filter with cut-off frequency of 20 Hz

<!-- image -->

Figure 8.9. Aligned QRST complexes after applying a low-pass second-order Butterworth filter with cut-off frequency of 20 Hz and rejection of outliers (Hotelling's T squared).

<!-- image -->

<!-- formula-not-decoded -->

The training set is placed into a single matrix T of dimensions N × M , so that N are the observations (number of beats) and M are the dimensions (number of time samples).

Figure 8.10. A submatrix of QRST-complex matrix containing all T waves of one channel

<!-- image -->

2. Calculate the empirical mean raw vector :The empirical mean along each dimension m = 1... M is calculated, see figure 8.11. Afterward, all computed mean values are placed into an empirical mean row vector u of dimensions M .

<!-- formula-not-decoded -->

Figure 8.11. An example of the empirical mean raw vector of the data matrix T

<!-- image -->

3. Calculate the deviations from the mean : The empirical mean row vector u is subtracted from each row of the data matrix T . Then a new mean-subtracted data matrix B ( N × M ) is derived, see figure 8.12.

<!-- formula-not-decoded -->

where h is a column vector of ones and size of N x 1 : h ( n ) = 1 for n = 1 . . . N ,

Figure 8.12. An example of the mean-subtracted data matrix of the original data matrix T

<!-- image -->

4. Find the covariance matrix : As illustrated before, the M × M empirical covariance matrix C is calculated from the outer product of the zero-centered matrix B with itself:

<!-- formula-not-decoded -->

where E is the expected value operator, ⊗ is the outer product operator, and ∗ is the conjugate transpose operator.

5. Find the eigenvectors and eigenvalues of the covariance matrix : This step will typically require the use of a computer-based algorithm for computing the eigenvalue matrix D and the eigenvector matrix V of the covariance matrix C :

<!-- formula-not-decoded -->

Matrix D will take the form of an M × M diagonal matrix, where D [ p, q ] = λ m for p = q = m is the m th eigenvalue of the covariance matrix C , and D [ p, q ] = 0 for p = q.

Matrix V , also of dimension M × M , contains M column vectors, each of length M ,

/negationslash

which represent the M eigenvectors of the covariance matrix C .

- The eigenvalues and eigenvectors are ordered and paired. The m th eigenvalue corresponds to the m th eigenvector.
6. Rearrange the eigenvectors and eigenvalues : The columns of the eigenvector matrix V and eigenvalue matrix D are sorted out in order of decreasing eigenvalues maintaining the correct pairings between the columns in each matrix.
7. Convert the source data to the new basis : The new basis is denoted as PCA-scores or the reconstruction parameter vectors (RPV). The projected vectors are the columns of the matrix Z ( N × M ), namely Z i 1 , Z i 2 , · · · , Z iM , where i = 1 ...N . The matrix Z is calculated by multiplying the eigenvector matrix with the zero-mean data matrix from the left as follows:

<!-- formula-not-decoded -->

The rows of Z correspond to the observations (number of beats), whereas the columns refer to the components or dimensions (number of time samples). The first PCA scores, corresponding the first column vector of the matrix Z , represent the deviation of T wave morphology to the mean T wave. Figure 8.13 shows the first PCA scores (or first RPV) versus T wave beat number representing the observations.

Figure 8.13. The first PCA scores (or first RPV) versus T wave beat number.

<!-- image -->

In fact, the projected PCA-scores or vectors represent the Karhunen-Lo` eve transform (KLT) of the data vectors in the columns of matrix T .

As next, the first PCA scores are analysed in order to assess the degree of variation for all T waves compared to their mean T wave, i.e. the beat-to-beat T-wave morphology variation throughout the whole channel.

## 8.1.2.3 Analysing the First PCA Scores

Since the first PCA scores represented in the first column vector of the matrix Z accounts for most of the variance in the data, analysis was carried out only on these scores so far. Standard deviation (SD) was used and applied on the first PCA scores as a simple linear measure to assess the beat-to-beat morphology variation. As the length of the first PCA score vector is N , the number of T waves in one channel, a window of length 60 with zero overlapping was chosen to scan this vector calculating the SD for the scores inside this window at each step. Finally, a series of SD values will come out and form a new vector called 'SD Vector'. High SD value represents high beat-to-beat PCA score variation , i.e. high beat-to-beat T-wave morphology variation, and vice versa for the low SD value. In order to get an overall measure of variation for each channel, the mean of the derived SD values was calculated.

## 8.1.3 Results

The method illustrated above for calculating the overall measure of variation was applied on every channel of all healthy subjects, see figure 8.14 and figure 8.15.

Furthermore, this overall measure of variation was calculated twice on every channel of TDP subjects. The first one measures T-wave overall variation from the beginning of the tape until TDP episode, see figure 8.16.

Whereas, the second one measures T-wave overall variation starting after TDP episode until the end of the tape, see figure 8.17.

The overall measure of variation for 84 useful channels from the healthy tapes are presented in table A.1, see Appendix A. Furthermore, the overall measure of variation before and after TDP episode for 20 TDP channels from the TDP tapes are presented in table A.2 and table A.3, respectively, see Appendix A.

The average value of the overall measure of variation for 84 useful channels from the healthy tapes was equal to 73.8119 ± 12.4222 and the average value of the overall measure of variation for T waves before TDP episode of 20 useful channels from the TDP tapes was equal to 241.9493 ± 168.3503 , whereas the average value of the overall measure of variation for T waves after TDP episode of 20 useful channels from the TDP tapes was equal to 145.7783 ± 86.3924 , see figure 8.18.

Since the SD values for all TDP tapes before and after the episode are available, it is useful to employ them in order to have a closer and more detailed information about the beat-to-beat T wave morphology variation before and after TDP episode. Therefore, the mean of SD values for all channels before and after TDP episode was calculated. Because every channel has a different number of SD windows before and after TDP, the SD windows for all channels before TDP were rearranged, so that they are right aligned to the last window just before TDP episode. On the other hand, the SD windows for all channels after TDP were kept left aligned to the first window just after TDP episode. The

calculation of the final mean SD values of similar windows did not take into calculation any possible missing SD values, i.e. missing windows . Figure 8.19 shows the final results.

## 8.1.4 Discussion and Conclusions

Figure 8.19 shows that the beat-to-beat morphology T-wave variation before TDP episode is remarkably higher than the normal level, more chaotic and increased by approaching the TDP episode. Figure 8.19 illustrates also that the T-wave beat-to-beat morphology variation after TDP episode is not as high as before TDP episode and is decreasing by receding away from TDP episode until it reaches the normal variation level. Referring to our results, detecting predisposition to TDP is possible some hours prior to TDP episode employing the normal level of T-wave variation derived by our calculation.

## 8.2 T-Wave Morphology Clustering

## 8.2.1 Introduction

The diagnosis of some cardiac diseases, like certain cardiac arrhythmias which occur occasionally, is often not reliable in short-time ECG recordings. In these cases the patient's ECG will therefore be recorded over a day-long period. Taking into account an average long-term recording of 24 hours, nearly 100000 ECG complexes have to be analysed [212]. Accomplishing this task manually is time-consuming, cumbersome and susceptible to failures. During otherwise constant periods, ectopic beats might be overlooked. Furthermore, the identification of similar signals spread over such a large time span is difficult for the human observer. Finally the results retrieved from different physicians sometimes show a significant variety.

Cluster analysis, also called segmentation analysis or taxonomy analysis, is a way to create groups of objects, or clusters, in such a way that the profiles of objects in the same cluster are very similar and the profiles of objects in different clusters are quite distinct [1].

The clustering techniques are designed to break the data set into two or more homogeneous groups. PCA is often used to reduce the data to a smaller number of transformed variables before the clustering is carried out. This is done partly to reduce the size of the computing problem and because the use of PCA scores help also to identify the characteristics of the clusters.

Figure 8.20 shows a scatter plot between the first three principal PCA scores respectively, extracted from T waves of the same long-time ECG signal, as described in section 8.1.2.2. In this plot, three main different 'clouds' are noticed. Since PCA scores represent descriptive parameters for T wave forms, these visible 'clouds' in figure 8.20 represent different T wave morphologies, i.e. different clusters.

For a human observer, detecting these three clusters is trivial, but computer algorithm has to apply rules that have to be worked out. Therefore, a computer-based method to detect different clusters from the first principal PCA scores was developed and is presented here in this section. The PCA scores are derived from T waves of a long-time ECG signal, as described in section 8.1.2.2. The number of principal PCA scores used for

the morphological feature extraction is chosen to be three, since they account for most of the variance from the input T wave signals.

Previous work on this subject has been done by Cuesta-Frau et al., who amongst other techniques incorporated wavelet-transformation and polygonal approximation coefficients to describe and cluster the individual QRST-complexes [213, 214].

Furthermore, Jankoswki et al. [215] developed a self-learning system, that tried to sort every QRST-complex of a certain Holter recording into one of four bins. The decision was based on 30 parameters that served as coefficients for a template function.

In general, data clustering algorithms can be hierarchical or partitional. Hierarchical algorithms find successive clusters using previously established clusters, whereas partitional algorithms determine all clusters at once, i.e. a single level of clusters. K-means algorithm is the typical algorithm for partitional clustering. It assigns each point to the cluster whose center, also called centroid, is nearest. The centroid is the point to which the sum of distances from all objects in that cluster is minimized and calculated as the arithmetic mean for each dimension separately over all the points in the cluster. In order to find the final centroids along with their corresponding clusters, a certain number of points should be first picked up from the data as primarily centroids. As the next step, the remaining elements have to be assigned to their nearest centroids. Subsequently, the centroids will get recalculated based on the new distribution. This may be repeated several times to improve the assignments. There are several ways to choose the starting centroids. More details on the first selection can be found in [216]. In fact, the result of partitional clustering depends to a large extent on the first selection of the points. Moreover, the partitional clustering algorithm is very time-consuming especially for long database, like long-time ECG. In contrast, hierarchical clustering algorithms can be much faster and provide much more stable results, which are independent on any primarily manually- or automatically-chosen centroids. Therefore, a hierarchical clustering algorithm was used on PCA scores in this work aiming to detect the different clusters of T waves in every single-channel ECG signal.

## 8.2.2 Method

## 8.2.2.1 Calculating the first three principal PCA scores

The first three principal PCA scores, corresponding to the first three column vectors of the matrix Z , as described in section 8.1.2.2, are computed from T waves of a long-time ECG signal. It should be mentioned that the alignment is carried out using the R peak of every heart beat. In this may also we ensured that changes of QT interval are detected. Figure 8.13 shows a 3D scatter plot for the first three PCA scores (or first three RPVs). The number of the points in this scatter plot is equal to the number of T waves and the length of every RPV. Every point in the plot represents one T wave and is called an object. In order to validate this step, 200 noisy half-sinus signals from 0 to π , with 90 samples each, were generated in four different groups regarding their amplitude, see figure 8.21. The first three principal PCA scores were computed afterward as described in section 8.1.2.2. Figure 8.22 is a 3D scatter plot of first three PCA scores corresponding to the input 200 sinus signals. Four groups of objects can be noticed from figure 8.22. These groups correspond in fact to the original half-sinus groups. In the following steps,

the procedure to cluster all objects in the 3D scatter PCA scores in different groups will be described.

## 8.2.2.2 Find the Similarity or Dissimilarity Between Every Pair of Objects

There are many ways to calculate a 'distance' between the heart beats, also called proximity. The two most popular methods to calculate the distance between group of points are the Euclidean distance and the city block metric .

1. Euclidean distance : It is similar to a line of sight. It's the shortest distance between two elements. Determining this distance for a pair of items - → x and - → y in an n -dimensional space is given as:

<!-- formula-not-decoded -->

2. City block metric : This method simply sums up the way, that has to be covered to get from element - → x to - → y when only paths parallel to the axes of the coordinate system are permitted.

<!-- formula-not-decoded -->

The distances between the objects in our method have been computed using the Euclidean distance.

## 8.2.2.3 Defining the Links Between Objects

Once the proximity between the objects has been computed, every pairs of objects, that are close together, will be linked into binary clusters, i.e. clusters made up of two objects. Afterward, these newly formed clusters will be linked to other objects to create bigger clusters until all the objects in the original 3D scatter PCA scores space are linked together in a hierarchical tree. In order to define if two subgroups are near enough to be combined to one bigger group, certain threshold on the distance between the centroids of these subgroups needs to be defined.

The hierarchical tree can be plotted in a so-called dendrogram, see figure 8.24.

In figure 8.24, the numbers along the horizontal axis represent the indices of the objects in the original 3D scatter PCA scores space. The links between objects are represented as upside down U-shaped lines. The height of the U indicates the distance between the objects.

## 8.2.2.4 Verifying the Cluster Tree

If the clustering is valid, the linking of objects in the cluster tree should have a strong correlation with the distances between objects. The cophenet function compares these two sets of values and computes their correlation, returning a value called the cophenetic correlation coefficient. The closer the value of the cophenetic correlation coefficient is

to 1, the better the clustering solution [1]. The cophenetic correlation coefficient ccc is usually used to compare the results of clustering the same data set using different distance calculation methods or clustering algorithms. Suppose Y is a vector containing the output of the distances between the objects and Z is a vector containing the links of these objects, ccc will be defined then as follows:

<!-- formula-not-decoded -->

where Y ij is the distance between objects i and j in Y , Z ij is the distance between objects i and j in Z , and where y and z are the average of Y and Z , respectively.

## 8.2.2.5 Creating Clusters

In order to define the final clusters, a certain threshold Thr needs to be chosen:

<!-- formula-not-decoded -->

where MaxL is the maximum distance between the objects in the dendrogram.

Afterward, an imaginary horizontal line with the height of Thr will be drawn across the dendrogram. This line will bisect n number of vertical U-shaped lines. The number n is then the number of clusters defined by this threshold and all the objects below one line will then belong to the same cluster.

This can be particularly evident in a dendrogram diagram where groups of objects are densely packed in certain areas and not in others. The inconsistency coefficient of the links in the cluster tree can identify these points where the similarities between objects change.

## 8.2.3 Result

The clustering method illustrated above was applied on T waves of 60 normal and 10 TDP two-channel tapes from different studies recorded during Dofetilide clinical trials (Pfizer, Inc.). Figure 8.25 shows a 3D colored scatter plot of the first three PCA scores of the figure 8.20. The objects with the same color in figure 8.25 belong to the same cluster. Figure 8.26 and 8.27 illustrate the result of clustering mapped back to real T waves, where similar T waves are plotted together and assigned with the similar color.

## 8.2.4 Discussion and Conclusion

In this section, a new method for feature extraction and clustering of occurring T-wave morphologies in long-term ECGs is presented. The use of PCA for the first task and hierarchical clustering for the latter has shown promising results. In order to apply this clustering method on long-time ECG signal, namely 24-hour long or longer, some techniques need to be implemented to split ECG signal into number of shorter ECG segments and then apply our clustering method on every segment and finally rearrange all results

together providing the final result for the complete ECG signal. From the dominant clusters representative examples may be obtained to characterize the whole dataset. Moreover, a significant reduction of data to be analysed is achieved by employing PCA and scores. Further evaluation is required to improve automatic threshold adjustment and the method should be applied to a larger number of datasets including more different pathological signals to verify the functionality.

Figure 8.14. The overall measure of variation from a healthy ECG (first channel): a) The healthy ECG signal. b) The corresponding first PCA scores. c) The corresponding SD vector and mean SD (the overall measure of variation).

<!-- image -->

QT 103, rna-24-5-C2, 81426 Deats

Figure 8.15. The overall measure of variation from a healthy ECG (second channel): a) The healthy ECG signal. b) The corresponding first PCA scores. c) The corresponding SD vector and mean SD (the overall measure of variation).

<!-- image -->

Figure 8.16. The overall measure of variation from a TDP ECG (before TDP episode): a) ECG signals before TDP episode. b) The corresponding first PCA scores. c) The corresponding SD vector and mean SD (the overall measure of variation).

<!-- image -->

Figure 8.17. The overall measure of variation from a TDP ECG (after TDP episode): a) ECG signals after TDP episode. b) The corresponding first PCA scores. c) The corresponding SD vector and mean SD (The overall measure of variation).

<!-- image -->

Figure 8.18. The average value of the overall measure of variation for 84 useful channels from the healthy tapes and for 20 useful channels from the TDP tapes.

<!-- image -->

Figure 8.19. The beat-to-beat morphology T-wave variation before and after TDP episode compared to the normal variation level derived from the healthy ECG signals

<!-- image -->

Figure 8.20. The first three principal Reconstruction Parameter Vectors (RPV) or PCA-scores plot as an example for cluster formation.

<!-- image -->

Figure 8.21. Two hundred noisy half-sinus signals from 0 to π with 90 samples each.

<!-- image -->

Figure 8.22. 3D scatter plot of the first three PCA scores, the first RPVs, corresponding to the 200 input Sinus signals shown in figure 8.21.

<!-- image -->

Figure 8.23. a) Euclidean distance. b) City block metric.

<!-- image -->

Figure 8.24. Cluster-Dendrogramm, Figure is adapted from [1]

<!-- image -->

Figure 8.25. Clustering result of the figure 8.20. The objects with the same color are belong to the same cluster

<!-- image -->

Figure 8.26. Clustering result of the figure 8.20 mapped back to real T waves. Similar T waves are plotted together and assigned with the similar color.

<!-- image -->

Figure 8.27. A top view of figure 8.26 showing the clustering result mapped back to real T waves. Here also, similar T waves are plotted together and assigned with the similar color.

<!-- image -->

## QRS Complex Morphology Analysis

## 9.1 Temporal &amp; Spatio-Temporal Analysis of QRS Complex

## 9.1.1 Introduction

In order to provide information on heart function, ECG signal and its components have been extensively analysed and used as powerful diagnostic tools. The morphology, amplitude and time of occurrence of QRS complex provide much information about the current contractile activity and state of the ventricles. The method, described in this section, is aimed to detect small changes in QRS morphology temporally and spatio-temporally as well as to examine the relationship between the these morphology changes and the heart rate as well as the respiration signal.

## 9.1.2 Databases Used

Six 64-channel IBT measured ECG signals are used. Their duration varies between one and five minutes. Table 9.1 shows more details about these signals, i.e. the number of beats (QRS complexes) in every signal and the number of channels used in the analysis.

Table 9.1: 64-channel IBT measured ECG signals along with their number of beats and channels used in the analysis

|   Signal No. No. of Channels Used No. of QRSs in each Channel |   Signal No. No. of Channels Used No. of QRSs in each Channel |   Signal No. No. of Channels Used No. of QRSs in each Channel |
|---------------------------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|
|                                                             1 |                                                            64 |                                                           332 |
|                                                             2 |                                                            64 |                                                           106 |
|                                                             3 |                                                            64 |                                                            57 |
|                                                             4 |                                                            64 |                                                            59 |
|                                                             5 |                                                            64 |                                                            69 |
|                                                             6 |                                                            64 |                                                            64 |

## 9.1.3 Defining Respiration &amp; Heart Rate Vectors

The respiration column vector is defined as follows:

<!-- formula-not-decoded -->

where N represents the total number of heart beats. The respiration vector is computed from the acquired discrete respiration signal S ( n ):

<!-- formula-not-decoded -->

where p is the beat number index and on p as well as off p are the corresponding QRS onset and offset instants. The heart rate column vector Hr = [ h 1 , · · · , h N ] T is computed from the R-R intervals derived from the delineation result as follows:

<!-- formula-not-decoded -->

where R p is the time location (in ms) of p th R peak, [217].

## 9.1.4 Data Preconditioning

First of all, the baseline wander is removed from every channel of every 64-channel ECG signal using the method presented in section 7.1. The next step is to localize the QRS complex boundaries and R peak for every beat in every channel. The single-channel delineation method, presented in section 7.4, is employed.

Afterward, QRS complexes of the same channel are extracted and assembled into one matrix, so that they represent the rows of that matrix. Furthermore, they are shifted toward right and left a certain small number of samples and finally aligned at the position corresponding to the highest correlation coefficient between this QRS complexes and a chosen template signal, which is in this case the average of all QRS complexes.

## 9.1.5 Temporal Analysis of QRS Complex

1. Assembling the input matrix for PCA : The input matrix for this analysis is the matrix obtained from a single channel of the databases described in section 9.1.2 after applying the preconditioning method. The input matrix is denoted here as QRS , which can be considered as a training set with N samples and each sample QRS i and can be expressed by a row vector with the size of M as follows:

<!-- formula-not-decoded -->

The training set is placed into a single matrix QRS T of dimensions N × M , so that N are the observations (number of beats) and M are the dimensions number of time samples), see figure 9.1.

2. Calculate the empirical mean raw vector : The empirical mean along each dimension m = 1... M is calculated, see figure 9.2. Afterward, all computed mean values are placed into an empirical mean row vector u of dimension M .

<!-- formula-not-decoded -->

Figure 9.1. An example of an input matrix QRS T containing all QRS complexes (57 complexes in this case) of one channel for a certain 64-channel ECG signal.

<!-- image -->

Figure 9.2. An example of the empirical mean of the data matrix QRS T presented in figure 9.1.

<!-- image -->

3. Calculate the deviations from the mean : The empirical mean row vector u is subtracted from each row of the data matrix QRS T . Then a new mean-subtracted data matrix B ( N × M ) is derived, see figure 9.3.

<!-- formula-not-decoded -->

where h is a column vector of ones and size of N x 1 : h ( n ) = 1 1 . . . N , for n =

Figure 9.3. An example of the mean-subtracted data matrix of the original data matrix T presented in figure 9.1.

<!-- image -->

4. Find the covariance matrix : As illustrated before, the M × M empirical covariance matrix C is calculated from the outer product of the zero-centered matrix B with itself:

<!-- formula-not-decoded -->

where E is the expected value operator, ⊗ is the outer product operator, and ∗ is the conjugate transpose operator.

5. Find the eigenvectors and eigenvalues of the covariance matrix : This step will typically require the use of a computer-based algorithm for computing the eigenvalue matrix D and the eigenvector matrix V of the covariance matrix C :

<!-- formula-not-decoded -->

Matrix D will take the form of an M × M diagonal matrix, where D [ p, q ] = λ m for p = q = m is the m th eigenvalue of the covariance matrix C , and D [ p, q ] = 0 for p = q.

Matrix V , also of dimension M × M , contains M column vectors, each of length M , which represent the M eigenvectors of the covariance matrix C .

/negationslash

The eigenvalues and eigenvectors are ordered and paired. The m th eigenvalue corresponds to the m th eigenvector.

6. Rearrange the eigenvectors and eigenvalues : The columns of the eigenvector matrix V and eigenvalue matrix D are sorted out in order of decreasing eigenvalues while maintaining the correct pairings between the columns in each matrix.
7. Compute the cumulative energy content for each eigenvector : The eigenvalues represent the distribution of the source data's energy among each of the eigenvectors, where the eigenvectors form a linear algebra basis for the data. The cumulative energy content g for the m th eigenvector is the sum of the energy content across all of the eigenvectors from 1 through m :

<!-- formula-not-decoded -->

From all the 64-channel ECG signals under study, it is found that the first three eigenvalues account for most of the variance and cumulative energy content, i.e. between 84% and 95% variance, see figure 9.4. Therefore, only the principal three eigenvectors and eigenvalues, m = 3, are taken into consideration for all channels under study in this analysis.

8. Select a subset of the eigenvectors as basis vectors : Save the first L = 3 columns of V as the M × 3 matrix W :

<!-- formula-not-decoded -->

Figure 9.4. The energy content for the first three eigenvectors of the mean-subtracted data matrix from the original data matrix QRS T presented in figure 9.1. The cumulative energy content for the first three eigenvalues here is equal to 91.6%.

<!-- image -->

Figure 9.5, figure 9.6 and figure 9.7 show the influence of the first, the second and the third eigenvetors (or principal components), namely PC1, PC2 and PC3, on the

empirical mean raw QRS vector u respectively. In other words, every principal component is first weighted by the factor of -100 and +100, and then added to the empirical mean raw QRS vector. Normally, the absolute values for the weighting factors used to reconstruct the QRS complexes back from the principal components and the empirical mean vector are much smaller than 100 in this study. However, the value '100' is used here just to show the direction of change and the influence of these principal components. Figure 9.5 illustrates that the first principal component tends to change the amplitude of the empirical mean raw QRS vector. Whereas, figure 9.6 and figure 9.7 show that PC2 and PC3 tend to shift the empirical mean raw QRS vector toward right and left and to move the isoelectric line of the empirical mean raw QRS vector upwards and downwards respectively. The direction of changes, shown in figure 9.5, figure 9.6 and figure 9.7, are observed in most of the ECG channels under study, i.e presented in section 9.1.2.

Figure 9.5. The influence of the first principal component, PC1, on the empirical mean raw QRS vector. This figure illustrates that the first principal component tends to change the amplitude of the empirical mean raw QRS vector.

<!-- image -->

9. Calculate PCA scores from the matrix W : The projected PCA scores are the columns of the matrix Z ( N × 3), namely Z i 1 , Z i 2 , Z i 3 in this case, where i = 1 ...N . The matrix Z is calculated by multiplying the eigenvector matrix with the zero-mean data matrix from the left as follows:

Figure 9.6. The influence of the second principal component, PC2, on the empirical mean raw QRS vector. This figure illustrates that the second principal component tends to shift the empirical mean raw QRS vector toward right and left.

<!-- image -->

Figure 9.7. The influence of the third principal component, PC3, on the empirical mean raw QRS vector. This figure illustrates that the third principal component tends to move the isoelectric line of the empirical mean raw QRS vector upwards and downwards.

<!-- image -->

<!-- formula-not-decoded -->

The rows of Z correspond to the observations, whereas the columns refer to the number of eigenvalues taken.

10. Define a new extended data matrix : A new matrix, CM = [ Z R Hr ], combining Z with respiration column vector R and and heart rate column vector Hr , is assembled. The matrix CM has the size of ( N × 5). Figure 9.8 shows the first three PCA scores along with the corresponding normalized respiration signal and heart rate signal for one channel of an ECG signal under study.
11. Calculating the correlation matrix of the matrix CM : The correlation matrix of the matrix CM of every channel in the ECG signal is calculated in order to discover all possible dependencies between the PCA scores and the respiration signal and the heart rate.
12. Calculating the average matrix CM aveT from all CM matrices : The average matrix CM aveT is calculated by averaging all CM matrices corresponding to all channels of the databases used and presented in section 9.1.2. Figure 9.9-a shows the correlation between the first three PCA scores and the respiration vector taken from the matrix CM aveT , whereas 9.9-b shows the correlation between the first three PCA scores and the heart rate vector also taken from the matrix CM aveT . It can be noticed from figure 9.9 that the first PCA has relatively a high correlation with both the heart rate and the respiration compared with the second and the third PCA scores.

Figure 9.8. The first three PCA scores along with the corresponding normalized respiration signal and heart rate signal for one channel of an ECG signal under study.

<!-- image -->

## 9.1.6 Spatio-Temporal Analysis of QRS Complex

The only difference between the spatio-temporal analysis of QRS complex, denoted as QRS ST , and the temporal one is the PCA input data matrix. There is only one spatiotemporal analysis matrix for every 64-channel ECG signal, whereas there are obviously 64

Figure 9.9. The correlation between the first three PCA scores with both the respiration signal and the heart rate vector taken from the matrix CM aveT in terms of the temporal analysis

<!-- image -->

temporal matrices for the same dataset. The spatio-temporal analysis matrix is obtained by concatenating horizontally all temporal analysis matrices for the ECG signal under study, so that it will have the size of N × M ′ , where, M ′ = n = ch ∑ n =1 M n , ch is the number of channels (here ch = 64) and M n is the number of columns (dimensions) in the temporal matrix QRS T for the channel number n . After defining the new spatio-temporal analysis input matrix for PCA, the steps 2 to 11, illustrated in section 9.1.5, will be applied on

Figure 9.10. The correlation between the first three PCA scores with both the respiration signal and the heart rate vector taken from the matrix CM aveST in terms of the spatio-temporal analysis

<!-- image -->

it. It was found here also that the first three eigenvalues account for most of the variance and cumulative energy content for all the 64-channel ECG signals used. After calculating the correlation matrix for every ECG signal, as described in step 11 of section 9.1.5, the average matrix CM aveST from all correlation matrices will be computed. Figure 9.10-a shows the correlation between the first three PCA scores and the respiration vector taken from the matrix CM aveST , whereas 9.10-b shows the correlation between the first three PCA scores and the heart rate vector also taken from the matrix CM aveST .

## 9.1.7 Discussion and Conclusion

The first PCA scores, corresponding to the first eigenvector, show a high degree of correlation with the heart rate and respiration pattern, as evident from the results of temporal and spatio-temporal analysis. Therefore, we can conclude that any change in heart rate, i.e. heart rate variability, or in respiration pattern will definitely lead to changes in QRS complex amplitude referring to the influence of the first principal component. The influences of the second and the third principal components might be based on the very small and tiny baseline wander cancellation error and the fine alignment error left in the signal during the preprocessing analysis. Based on the temporal analysis and spatio-temporal analysis presented so far, more research on QRS complex morphology fluctuations should carried out in the future. For example, the analysis could be extended to discover how the ECG pattern typically changes with blood pressure or any other useful entries, like QT interval, QTc interval, etc...

Furthermore, the same method could be also applied on ECG signals of patients, having different types of cardiac disorders (case of Ischemia, Ventricular Tachycardia, etc..), aiming to extract any diagnostic pattern typical to those diseases. More investigations could be done during higher levels of heart rate variability and during ECG stress test measurements. It is also important to mention that the beat-to-beat variation of QRS complex obtained with this analysis for different heart diseases is carrying also very useful diagnostic information, especially when analysing Atrial Fibrillation (AF) ECG signals.

## 9.2 Predicting QRS Complex

## 9.2.1 Introduction

In this section a novel method for estimating future QRS complexes of patients from the existing ones in their ECG signals is presented. It is based on using and investigating the scores of PCA. The aim of this analysis is to predict and estimate how the morphology of the future QRS complexes of an individual might appear, i.e. prediction for the ventricular electrical activity of the patient in the future. In other words, any trend, leading to long term changes that are dangerous for the patient, can be detected in a very early phase. That is, any sudden change can be immediately detected and can lead to a very fast alarm. The method is based on the temporal analysis procedure presented in section 9.1.5, therefore it can be applied on any single-channel ECG signal.

## 9.2.2 Single-Channel ECG Signal Preconditioning

First of all, the baseline wander is removed from the ECG signal using the method presented in section 7.1. Then, QRS complex boundaries and R peak for every beat will be localized using the single-channel delineation method, presented in section 7.4. Afterwards, QRS complexes are extracted and assembled in one matrix, so that they represent the rows of that matrix. Furthermore, the fine alignment method, presented in section 7.7, will be applied on the extracted QRS complexes generating the input matrix QRS T for the further analysis using PCA. This input matrix has the size of N × M , as described already, where N are the observations and M are the dimensions.

## 9.2.3 Method

1. Calculate PCA scores : The procedural steps 2 to 9, illustrated in section 9.1.5, will be applied here on the input matrix QRS T in order to calculate PCA scores. The number of PCA scores is equal to L , i.e. the number of selected eigenvalues, (see section 9.1.5). In the method, only the principal L eigenvalues, whose cumulative energy content account for at least 97% variance, is chosen, (see figure 9.11 as an example).
2. first degree polynomial fitting for every PCA scores : each chosen PCA scores will undergo a first-order polynomial fitting technique in a least-squares sense [218]. Finally, two polynomial coefficients, representing a line, will be obtained for every PCA scores. The function, characterizing one line corresponding one PCA scores, is called estimated function . The number of samples used to calculate every estimated function is equal to N , the number of QRS complexes (observations) in the channel, see section 9.1.5). Figure 9.12
3. Estimating future QRS complex : First of all, let us suppose that we need to estimate the ( N +1) th QRScomplex and that six eigenvalues and six eigenvectors are chosen L = 6, i.e. six PCA scores, namely Z i 1 , · · · , Z i 6 , and six estimated functions, denoted as f 1 , · · · , f 6 respectively. The six eigenvectors represent actually the column vectors of the submatrix W of size M × 6, see section 9.1.5. In order to calculate the ( N +1) th QRS complex, denoted as the row vector ˆ QRS N +1 , the values of the estimation functions at N +1 are first calculated, i.e. f 1 ( N +1), · · · , f 6 ( N +1), and put in a row vector F of size 1 × 6. Afterwards, the following equation is used:

Figure 9.11. The energy content for the first six eigenvectors, whose cumulative energy content accounts 97.8517% from the whole variance. The eigenvectors are calculated from the matrix QRS T of a single-channel ECG from the database presented in section 9.1.2.

<!-- image -->

Figure 9.12. The first degree polynomial fitting for the first PCA scores. The first PCA scores, plotted in blue stars, are calculated from a matrix QRS T of a single-channel ECG from the database presented in section 9.1.2. The corresponding estimated function is plotted in red.

<!-- image -->

<!-- formula-not-decoded -->

where u is the empirical mean row vector, described in section 9.1.5. The equation 9.12 is derived from the equation 5.48. The same procedure will be repeated, when needed, for ˆ QRS N +2 , ˆ QRS N +3 , and so on...

## 9.2.4 Validation

The QRS complex prediction method is evaluated using the 64-channel ECG signals described in section 9.1.2. Only half of the QRS complexes from each channel are taken under consideration for our PCA-based estimator. In other words, the first half of QRS complexes in every channel builds the input matrix QRS T of that channel. Afterward, the other half of QRS-complexes of every channel were predicted using the method described above. Thereafter, the similarity between every real measured QRS complex and the corresponding predicted one is calculated by means of the correlation coefficients technique as well as the absolute value of the error and the RMS error. The average value of similarities and errors along the predicted QRS complexes in every channel is computed. Table 9.2 illustrates the mean similarity values as well as the mean error values taken for each ECG signal.

Furthermore, the average similarity, absolute error and RMS error for all of the six databases, are found to be 99.3256 % , 20.7452 µV and 22.4705 µV respectively.

Figure 9.13 shows an example of a real QRS complex taken from one of the ECG signals used and its corresponding predicted one.

Table 9.2. The average value of similarities and errors along the predicted QRS complexes in every channel for each ECG signal, described in section 9.1.2.

|   Signal |   QRS No. | QRS Taken   | Predicted QRS   | Similarity   | Error      | RMS Error   |
|----------|-----------|-------------|-----------------|--------------|------------|-------------|
|        1 |       332 | First 166   | last 166        | 98.9742 %    | 16.6729 µV | 17.5875 µV  |
|        2 |       106 | First 53    | Last 53         | 98.5571 %    | 32.4993 µV | 39.3256 µV  |
|        3 |        57 | First 29    | Last 28         | 99.7507 %    | 19.7252 µV | 19.6019 µV  |
|        4 |        59 | First 30    | Last 29         | 99.641 %     | 23.0615 µV | 25.8759 µV  |
|        5 |        69 | First 35    | Last 34         | 99.3577 %    | 16.7292 µV | 17.4826 µV  |
|        6 |        64 | First 32    | Last 32         | 99.673 %     | 15.7831 µV | 14.9497 µV  |

Figure 9.13. An example of a real QRS complex plotted in blue line and taken from one of the ECG signals used and its corresponding predicted or estimated one plotted in red dots.

<!-- image -->

## 9.2.5 Discussion and Conclusion

This novel approach shows a very high similarity in morphology between the estimated QRS complexes and the corresponding real signals as well as relatively small reconstruction errors. The method was evaluated on different QRS complex morphologies, since 64-channel ECG signals were used. Therefore, the high efficiency, accuracy, and authenticity can be considered as properties of this new method. On the other hand, this method could be improved by applying more ECG signals of healthy people as well as patients and by comparing the results in both cases. The method may be evaluated also on longer ECG signal, like Holter ECG signal. Breathing effects and heart rate were not included in this study, but it will be considered as one of the improvements of this technique in the future. This technique may allow for some useful clinical implications. The output signals of our estimator could be used to predict the changes in ECG that the patient might have in the near future. Another application of this new method is to analyse the morphology of the input signals by observing the PCA scores. When all input signals

look similar relatively to each other and to the mean signal, PCA scores will have values around zero with certain positive and negative limits (see Figure 5). On the other hand, when one input signal or look more different to the mean signal, its or their corresponding PCA scores will have relative higher values compared to the others. Therefore, by analyzing PCA scores obtained from a short-term ECG signal (few minutes) and after setting corresponding individual thresholds for every patient and channel, our method will be able to detect any input signal that looks different to the previous inputs and their mean. Moreover, an alarm could be generated if any serious change in the waveform is detected. A continuous update of this ECG analysis allows for immediate warning in case of any small change in the state of the heart.

## A

## Appendix A

Table A.1: The overall measure of variation for 84 useful channels from the healthy tapes

| Normal signal (QT103 study Pfizer Inc.)   |   Overall measure of variation |
|-------------------------------------------|--------------------------------|
| rnd-03-1-c1                               |                        65.9815 |
| rnd-03-1-c2                               |                        67.0296 |
| rnd-03-3-c2                               |                        95.2607 |
| rnd-03-5-c1                               |                        73.5684 |
| rnd-03-5-c2                               |                        61.2363 |
| rnd-04-1-c1                               |                        77.1577 |
| rnd-04-1-c2                               |                        94.9152 |
| rnd-04-3-c1                               |                        89.0863 |
| rnd-04-3-c2                               |                        84.0749 |
| rnd-04-5-c1                               |                        75.4639 |
| rnd-04-5-c2                               |                        84.3077 |
| rnd-05-3-c1                               |                        63.8235 |
| rnd-13-1-c1                               |                        84.3759 |
| rnd-13-1-c2                               |                        79.3576 |
| rnd-13-3-c1                               |                        91.854  |
| rnd-13-3-c2                               |                        98.3884 |
| rnd-14-1-c1                               |                        54.6886 |
| rnd-14-1-c2                               |                        75.7053 |
| rnd-14-3-c1                               |                        62.0313 |
| rnd-15-1-c1                               |                        84.7752 |
| rnd-15-1-c2                               |                        77.18   |
| rnd-15-3-c1                               |                        70.4363 |
| rnd-15-3-c2                               |                        96.5308 |
| rnd-16-1-c1                               |                        84.0083 |
| rnd-16-1-c2                               |                        80.7156 |
| rnd-16-3-c1                               |                        70.2716 |
| rnd-17-3-c1                               |                        88.3706 |

Continued on next page

| Normal Signal (QT103 study Pfizer Inc.)   | Overall measure of variation   |
|-------------------------------------------|--------------------------------|
| rnd-17-3-c2                               | 67.3121                        |
| rnd-18-5-c1                               | 67.6                           |
| rnd-18-5-c2                               | 98.9605                        |
| rnd-19-1-c1                               | 61.8506                        |
| rnd-19-1-c2                               | 84.6877                        |
| rnd-19-3-c1                               | 60.908                         |
| rnd-19-5-c1                               | 70.2042                        |
| rnd-24-1-c1                               | 63.699                         |
| rnd-24-1-c2                               | 68.9028                        |
| rnd-24-3-c1                               | 64.6461                        |
| rnd-24-3-c2                               | 58.7963                        |
| rnd-24-5-c1                               | 61.2528                        |
| rnd-24-5-c2                               | 56.2113                        |
| rnd-26-1-c1                               | 54.2149                        |
| rnd-26-3-c1                               | 57.3143                        |
| rnd-26-3-c2                               | 95.2085                        |
| rnd-26-5-c1                               | 75.007                         |
| rnd-26-5-c2                               | 84.5494                        |
| rnd-27-1-c1                               | 69.8521                        |
| rnd-27-3-c1                               | 71.4082                        |
| rnd-27-5-c1                               | 59.4461                        |
| rnd-28-1-c1                               | 72.165                         |
| rnd-28-1-c2                               | 69.2988                        |
| rnd-28-3-c1                               | 68.3608                        |
| rnd-28-3-c2                               | 57.6045                        |
| rnd-28-5-c1                               | 66.6989                        |
| rnd-28-5-c2                               | 53.9872                        |
| rnd-29-1-c1                               | 52.0676                        |
| rnd-29-3-c1                               | 64.479                         |
| rnd-29-3-c2                               | 89.3713                        |
| rnd-29-5-c1                               | 73.2251                        |
| rnd-29-5-c2                               | 93.619                         |
| rnd-31-1-c1                               | 77.0803                        |
| rnd-31-1-c2                               | 57.2647                        |
| rnd-31-3-c1                               | 67.147                         |
| rnd-31-3-c2                               | 57.3003                        |
| rnd-31-5-c1                               | 88.2159                        |
| rnd-31-5-c2                               | 62.1303                        |
| rnd-32-1-c1                               | 70.6327                        |
| rnd-32-1-c2                               | 91.23                          |
| rnd-32-3-c1 rnd-32-3-c2                   | 55.4798 73.6067                |

Continued on next page

| Normal Signal (QT103 study Pfizer   |   Overall measure of variation |
|-------------------------------------|--------------------------------|
| rnd-32-5-c1                         |                        61.2699 |
| rnd-32-5-c2                         |                        76.7639 |
| rnd-34-1-c1                         |                        88.655  |
| rnd-34-5-c1                         |                        76.9953 |
| rnd-35-1-c1                         |                        92.7715 |
| rnd-35-1-c2                         |                        78.62   |
| rnd-35-3-c1                         |                        75.561  |
| rnd-35-3-c2                         |                        68.1398 |
| rnd-36-1-c2                         |                        78.4533 |
| rnd-36-3-c1                         |                        77.9659 |
| rnd-36-3-c2                         |                        80.9563 |
| rnd-36-5-c1                         |                        79.0237 |
| MEAN ALL                            |                        73.8119 |
| SD ALL                              |                        12.4222 |

Table A.2: the overall measure of variation before TDP episode for 20 TDP channels from the TDP tapes

| TDP signal (different study Pfizer Inc.)   |   Overall measure of variation |
|--------------------------------------------|--------------------------------|
| CL-c1                                      |                        210.071 |
| CL-c2                                      |                        157.996 |
| EBP-c1                                     |                        136.885 |
| EBP-c2                                     |                        164.9   |
| H-B-c1                                     |                        744.218 |
| H-B-c2                                     |                        294.461 |
| JF-c1                                      |                        195.062 |
| JF-c2                                      |                        200.387 |
| MD-c1                                      |                        118.006 |
| MD-c2                                      |                        125.47  |
| MS-c1                                      |                        572.799 |
| MS-c2                                      |                        259.943 |
| R-B-c1                                     |                        222.184 |
| R-B-c2                                     |                        276.374 |
| R-B-c-c1                                   |                        149.41  |
| R-B-c-c2                                   |                        133.907 |
| SBA-c1                                     |                        179.231 |
| SBA-c2                                     |                        476.914 |
| VL-c1                                      |                        120.63  |
| VL-c2                                      |                        100.138 |
| MEAN ALL                                   |                        241.949 |
| SD ALL                                     |                        168.35  |

Table A.3: The overall measure of variation after TDP episode for 20 TDP channels from the TDP tapes

| TDP signal (different study Pfizer Inc.)   |   Overall measure of variation |
|--------------------------------------------|--------------------------------|
| CL-c1                                      |                       189.32   |
| CL-c2                                      |                       127.221  |
| EBP-c1                                     |                       191.093  |
| EBP-c2                                     |                       150.585  |
| H-B-c1                                     |                       173.216  |
| H-B-c2                                     |                        95.6541 |
| JF-c1                                      |                        96.8325 |
| JF-c2                                      |                        90.4643 |
| MD-c1                                      |                        70.3808 |
| MD-c2                                      |                        93.274  |
| MS-c1                                      |                       149.81   |
| MS-c2                                      |                        62.4312 |
| R-B-c1                                     |                       158.077  |
| R-B-c2                                     |                       195.72   |
| R-B-c-c1                                   |                        66.2288 |
| R-B-c-c2                                   |                       118.037  |
| SBA-c1                                     |                       198.492  |
| SBA-c2                                     |                       460.119  |
| VL-c1                                      |                       109.09   |
| VL-c2                                      |                       119.522  |
| MEAN ALL                                   |                       145.778  |
| SD ALL                                     |                        86.3924 |

## Bibliography

1. I. The MathWork, Statistics Toolbox User's Guide . The MathWork, Inc., 2005.
2. W. Bargmann, 'Bau des Herzens,' in Das Herz des Menschen (W. Bargmann and W. Doerr, eds.), pp. 88164, Stuttgart: Georg Thieme Verlag, 1963.
3. R. H. Anderson and A. E. Becker, Anatomie des Herzens . Stuttgart: Georg Thieme Verlag, 1982.
4. H. Gray and W. H. Lewis, Anatomy of the human body . Philadelphia: Lea &amp; Febiger, 20 ed., 1918.
5. 'www.tmc.edu/thi/anatomy.html,'
6. R. P. J. Malmivuo, BIOELECTROMAGNETISM Principles and Applications of Bioelectric and Biomagnetic Fields . New York: Oxford University Press, 1995.
7. J. Schrader, 'Das Herz,' in Lehrbuch der Physiologie (R. Klinke and S. Silbernagl, eds.), ch. 7, pp. 109-144, Stuttgart, New York: Thieme, 2001.
8. H. Antoni,'Mechanik der Herzaktion,'in Physiologie des Menschen (R. F. Schmidt, G. Thews, and F. Lang, eds.), ch. 22, pp. 448-471, Berlin, Heidelberg, New York: Springer, 2000.
9. E. Bauereisen, 'Normale Physiologie des Herzens,' in Das Herz des Menschen (W. Bargmann and W. Doerr, eds.), ch. 7, pp. 313-354, Stuttgart: Georg Thieme Verlag, 1963.
10. 'http://en.wikipedia.org/wiki/Image:Diagramfheumaneart28cropped%29.svg.'
11. 'http://www.bris.ac.uk/Depts/Physiology/ugteach/ugindex/m1ndex/nmut3/page2.htm.'
12. J. Dudel, 'Grundlagen der Zellphysiologie,' in Physiologie des Menschen (R. F. Schmidt, G. Thews, and F. Lang, eds.), ch. 1, pp. 3-19, Berlin, Heidelberg, New York: Springer, 2000.
13. C. W. Balke, E. Marb´ an, and B. O'Rourke, 'Calcium channels: Structure, function, and regulation,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 2, pp. 8-21, Philadelphia: W. B. Saunders Company, 3 ed., 1999.
14. T. J. Kamp, Z. Zhou, S. Zhang, J. C. Makielski, and C. T. January,'Pharmacology of L- and T-type calcium channels in the heart,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 17, pp. 141-156, Philadelphia: W. B. Saunders Company, 3 ed., 1999.
15. D. M. Bers, 'Cardiac calcium channels,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 2, pp. 10-18, Philadelphia: W. B. Saunders Company, 4 ed., 2004.
16. X. Chen and S. R. Houser, 'Pharmacology of L-type and T-type calcium channels in the heart,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 16, pp. 133-142, Philadelphia: W. B. Saunders Company, 4 ed., 2004.
17. R. L. Rasmusson,'Pharmacology of potassium channels,'in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 18, pp. 156-167, Philadelphia: W. B. Saunders Company, 3 ed., 1999.
18. G. Y. Oudit, R. J. Ramirez, and P. H. Backx, 'Voltage-regulated potassium channels,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 3, pp. 19-32, Philadelphia: W. B. Saunders Company, 4 ed., 2004.
19. M. C. Sanguinetti and M. Tristani-Firouzi, 'Gating of cardiac delayed rectifier K + channels,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 10, pp. 88-95, Philadelphia: W. B. Saunders Company, 4 ed., 2004.
20. S. J. Carroll, J. Kurokawa, and R. S. Kass, 'KCNQ1/KCNE1 macromolecular signaling complex: Channel microdomains and human disease,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 17, pp. 143-150, Philadelphia: W. B. Saunders Company, 4 ed., 2004.

21. M. Dellmar, G. E. Morley, J. F. Ek-Vitorin, D. Francis, N. Homma, K. Stergiopoulos, A. Lau, and S. M. Taffet, 'Intracellular regulation of the cardiac gap junction channel connexin43,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 15, pp. 126-132, Philadelphia: W. B. Saunders Company, 3 ed., 1999.
22. M. Delmar, H. S. Duffy, P. L. Sorgen, S. M. Taffet, and D. C. Spray, 'Molecular organization and regulation of the cardiac gap junction channel connexin43,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 8, pp. 66-76, Philadelphia: W. B. Saunders Company, 4 ed., 2004.
23. J. E. Saffitz and K. A. Yamada, 'Gap junction distribution in the heart,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 21, pp. 271-277, Philadelphia: W. B. Saunders Company, 3 ed., 1999.
24. A. P. Moreno, V. Hayrapetyan, G. Zhong, A. D. Martinez, and E. C. Beyer, 'Homometric and heterometric gap junctions,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 14, pp. 120-126, Philadelphia: W. B. Saunders Company, 4 ed., 2004.
25. J. W. Kimball, Biology . Reading, Massachusetts; Menlo Park, California: Addison-Wesley, 5 ed., 1983.
26. A. Noma and N. Tsuboi, 'Dependence of junctional conductance on proton, calcium and magnesium ions in cardiac paired cells of guinea-pig,' J. Physiol. , vol. 382, pp. 193-211, 1987.
27. V. M. Unger, N. M. Kumar, N. B. Gilula, and M. Yeager, 'Three-dimensional structure of a recombinant gap junction membrane channel,' Science , vol. 283, pp. 1176-1180, 1999.
28. H. J. Jongsma and M. B. Rook, 'Biophysics of cardiac gap junction channels,' in Cardiac Electrophysiology. From Cell to Bedside (D. P. Zipes and J. Jalife, eds.), ch. 14, pp. 119-125, Philadelphia: W. B. Saunders Company, 3 ed., 1999.
29. S. Verheule, M. J. A. van Kempen, P. H. J. A. te Welscher, B. R. Kwak, and H. J. Jongsma,'Characterization of gap junction channels in adult rabbit atrial and ventricular myocardium,' Circ. Res. , vol. 80, pp. 673-681, 1997.
30. L. Bate and M. Gardiner, 'Expert Review of Molecular Medicine, http://wwwermm.cbcu.cam.ac.uk/9900143Xa.pdf,' Cambridge University Press , 1999.
31. 'http://www.coheadquarters.com/PennLibr/MyPhysiology/myocell/Muscle1x.jpg.'
32. 'http://www.cs.wright.edu/ dkender/bme422/sarcmr2.gif.'
33. L. S¨ ornmo and P. Laguna, Bioelectrical Signal Processing in Cardiac and Neurological Applications . Linacre House Jordan Hill Oxford OX2 8DP United Kingdom: Elsevier, 1 ed., 2005.
34. C. D. Werner, F. B. Sachse, and D
35. 'http://en.wikipedia.org/wiki/Actionotential.'
36. 'http://www.cvphysiology.com/Arrhythmias/A007.htm.'
37. 'http://www.mfi.ku.dk/.'
38. 'http://www.cvphysiology.com/Cardiac%20Function/CF022.htm.'
39. V. Fuster, R. W. Alexander, R. A. O'Rourke, and R. Roberts, Hurst's The Heart . McGraw-Hill Professional, 11 ed., 2004.
40. B. Surawicz and T. Knilans, Chou's Electrocardiography in Clinical Practice . Philadelphia: McGraw-Hill Professional, 5 ed., 2001.
41. J. Barker, The unipolar Electrocardiogram: A Clinical Interpretation . Chicago: Year Book Medical Publishers, 1952.
42. 'http://www.cvrti.utah.edu/ macleod/bioen/be6000/labnotes/ecg/figures/limbleads.gif.'
43. R. E. Mason and I. Likar, 'A new system of multiple-lead exercise electrocardiography,' Am Heart J , vol. 71, pp. 196-205, Feb 1966.
44. V. F. J. Froelicher, R. Wolthius, N. Keiser, A. Stewart, J. Fischer, M. R. J. Longo, J. H. Triebwasser, and M. C. Lancaster, 'A comparison of two bipolar exercise electrocardiographic leads to lead V5,' Chest , vol. 70, pp. 611-616, Nov 1976.
45. L. T. Sheffield, R. Prineas, H. C. Cohen, A. Schoenberg, and V. Froelicher, 'The quest for optimal electrocardiography. Task Force II: Quality of electrocardiographic records,' Am J Cardiol , vol. 41, pp. 146-157, Jan 1978.
46. P. W. Macfarlane and T. D. V. Lawrie, Comprehensive Electrocardiology: Theory and Practice in Health and Disease . Pergamon, 1989.
47. M. Potse, Integrated Electrocardiographic Mapping . Amsterdam: Thela Thesis, 2001.

48. R. C. Barr, M. S. Spach, and G. S. Herman-Giddens, 'Selection of the number and positions of measuring locations for electrocardiography,' IEEE Trans Biomed Eng , vol. 18, pp. 125-138, Mar 1971.
49. F. Kornreich, 'The missing waveform information in the orthogonal electrocardiogram (Frank leads). I. Where and how can this missing waveform information be retrieved?,' Circulation , vol. 48, pp. 984-995, Nov 1973.
50. B. Taccardi and B. Punske, 'Body Surface And Epicardial ECG Mapping: State Of The Art And Future Perspectives,' International Journal of Bioelectromagnetism , vol. 4, no. 2, pp. 91-94, 2002.
51. R. L. Lux, C. R. Smith, R. F. Wyatt, and J. A. Abildskov, 'Limited lead selection for estimation of body surface potential maps in electrocardiography,' IEEE Trans Biomed Eng , vol. 25, pp. 270-276, May 1978.
52. P. R. Maroko, P. Libby, J. W. Covell, B. E. Sobel, J. J. Ross, and E. Braunwald, 'Precordial S-T segment elevation mapping: an atraumatic method for assessing alterations in the extent of myocardial ischemic injury. The effects of pharmacologic and hemodynamic interventions,' Am J Cardiol , vol. 29, pp. 223-230, Feb 1972.
53. K. M. Fox, A. P. Selwyn, and J. P. Shillingford, 'Projection of electrocardiographic signs in praecordial maps after exercise in patients with ischaemic heart disease,' Br Heart J , vol. 42, pp. 416-421, Oct 1979.
54. K. Fox, J. Deanfield, R. Ribero, D. England, and C. Wright, 'Projection of ST segment changes on to the front of the chest. Practical implications for exercise testing and ambulatory monitoring,' Br Heart J , vol. 48, pp. 555-559, 1982.
55. D. M. Monro, R. A. Guardo, P. J. Bourdillon, and J. Tinker, 'A Fourier technique for simultaneous electrocardiographic surface mapping,' Cardiovasc Res , vol. 8, pp. 688-700, Sep 1974.
56. D. M. Monro, 'Interpolation methods for surface mapping,' Comput Programs Biomed , vol. 11, pp. 145-157, Apr 1980.
57. D. M. Monro,'Interpolation by fast Fourier and Chebyshev transforms,' Int. J. Num. Methods Eng. , vol. 14, no. 11, pp. 1679-1692, 1979.
58. N. J. HOLTER, 'New method for heart studies,' Science , vol. 134, pp. 1214-1220, Oct 1961.
59. L. T. Sheffield, A. Berson, D. Bragg-Remschel, P. C. Gillette, R. E. Hermes, L. Hinkle, H. Kennedy, D. M. Mirvis, and C. Oliver, 'Recommendations for standards of instrumentation and practive in the use of ambulatory electrocardiography. The Task Force of the Committee on Electrocardiography and Cardiac Electrophysiology of the Council on Clinical Cardiology,' Circulation , vol. 71, pp. 626A-636A, Mar 1985.
60. R. N. MacAlpin, 'Correlation of the location of coronary arterial spasm with the lead distribution of ST segment elevation during variant angina,' Am Heart J , vol. 99, pp. 555-564, May 1980.
61. A. A. Quyyumi, L. Mockus, C. Wright, and K. M. Fox, 'Morphology of ambulatory ST segment changes in patients with varying severity of coronary artery disease. Investigation of the frequency of nocturnal ischaemia and coronary spasm,' Br Heart J , vol. 53, pp. 186-193, Feb 1985.
62. 'http://www.cvphysiology.com/Arrhythmias/A009.htm.'
63. 'http://www.lond.ambulance.freeuk.com/ecg/ECG.htmU%20Wave.'
64. F. Moleiro, A. Castellanos, J. Diaz, and R. Myerburg,'Dynamics of the QT intervals encompassing secondary repolarization abnormalities duringsudden but transient lengthening of the RR intervals,' Am J Cardiol , pp. 883-885, 2003.
65. M. Malik, 'Is there a physiologic QT/RR relationship?,' J Cardiovasc Electrophysiol , vol. 13, pp. 1219-1221, Dec 2002. Comment.
66. H. Bazett, 'An analysis of the time-relations of electrocardiograms,' heart , vol. 7, pp. 353-370, 1920.
67. A. Castellanos, F. Moleiro, G. Lopera, H. Huikuri, A. J. Interian, and R. J. Myerburg, 'Dynamics of the uncorrected QT interval during vagal-induced lengthening of RR intervals,' Am J Cardiol , vol. 86, pp. 13901392, Dec 2000.
68. C. P. Day, J. M. McComb, and R. W. Campbell,'QT dispersion: an indication of arrhythmia risk in patients with long QT intervals,' Br Heart J , vol. 63, pp. 342-344, Jun 1990.
69. A. van Oosterom, 'Genesis of the t wave as based on an equivalent surface source model,' J. Electrocardiol. , vol. 34, no. Suppl, pp. 217-27, 2001.
70. 'http://sprojects.mmi.mcgill.ca/cardiophysio/EKGSTsegment.htm.'
71. H. Traberg, 'Marriott's Practical Electrocardiography,' N Engl J Med , vol. 332, no. 10, pp. 690-, 1995.
72. E. O. Robles de Medina, 'Clinical Electrocardiography : Antoni Bayes de Luna.,' Circulation , vol. 100, no. 5, pp. 567-, 1999.
73. M. Malik and A. J. Camm, 'Heart Rate Variability ,' Futura, Armonk, New York , 1995.

74. R. E. Kleiger, J. P. Miller, J. T. J. Bigger, and A. J. Moss,'Decreased heart rate variability and its association with increased mortality after acute myocardial infarction,' Am J Cardiol , vol. 59, pp. 256-262, Feb 1987.
75. R. G. Mark, Clinical Eelectrocardiography And Arrhythmias . USA: Massachusetts Institute of Technology, 2004.
76. 'http://sprojects.mmi.mcgill.ca/cardiophysio/wolffparkinsonwhite.htm.'
77. 'http://en.wikipedia.org/wiki/Heartlock.'
78. 'http://en.wikipedia.org/wiki/Ischaemiceartisease.'
79. 'http://www.webhealthcentre.com/centers/heart.asp.'
80. F. G. Akar, G.-X. Yan, C. Antzelevitch, and D. S. Rosenbaum, 'Unique topographical distribution of M cells underlies reentrant mechanism of torsade de pointes in the long-QT syndrome,' Circulation , vol. 105, pp. 1247-1253, Mar 2002.
81. M. E. Curran, I. Splawski, K. W. Timothy, G. M. Vincent, E. D. Green, and M. T. Keating, 'A molecular basis for cardiac arrhythmia: HERG mutations cause long QT syndrome,' Cell , vol. 80, pp. 795-803, Mar 1995.
82. J. Wei, D. W. Wang, M. Alings, F. Fish, M. Wathen, D. M. Roden, and A. L. J. George, 'Congenital long-QT syndrome caused by a novel mutation in a conserved acidic domain of the cardiac Na+ channel,' Circulation , vol. 99, pp. 3165-3171, Jun 1999.
83. P. T. Ellinor, D. J. Milan, and C. A. MacRae, 'Risk stratification in the long-QT syndrome,' N Engl J Med , vol. 349, pp. 908-909, Aug 2003. Comment.
84. 'http://en.wikipedia.org/wiki/LongTyndrome.'
85. W. Shimizu and C. Antzelevitch, 'Sodium Channel Block With Mexiletine Is Effective in Reducing Dispersion of Repolarization and Preventing Torsade de Pointes in LQT2 and LQT3 Models of the Long-QT Syndrome,' Circulation , vol. 96, no. 6, pp. 2038-2047, 1997.
86. P. J. Schwartz, A. J. Moss, G. M. Vincent, and R. S. Crampton, 'Diagnostic criteria for the long QT syndrome. An update,' Circulation , vol. 88, pp. 782-784, Aug 1993.
87. S. J. Compton, R. L. Lux, M. R. Ramsey, K. R. Strelich, M. C. Sanguinetti, L. S. Green, M. T. Keating, and J. W. Mason, 'Genetically defined therapy of inherited long-QT syndrome. Correction of abnormal repolarization by potassium,' Circulation , vol. 94, pp. 1018-1022, Sep 1996.
88. M. Tristani-Firouzi, J. L. Jensen, M. R. Donaldson, V. Sansone, G. Meola, A. Hahn, S. Bendahhou, H. Kwiecinski, A. Fidzianska, N. Plaster, Y.-H. Fu, L. J. Ptacek, and R. Tawil, 'Functional and clinical characterization of KCNJ2 mutations associated with LQT7 (Andersen syndrome),' J. Clin. Invest. , vol. 110, no. 3, pp. 381-388, 2002.
89. 'http://en.wikipedia.org/wiki/Brugadayndrome.'
90. K. Hong, A. Berruezo-Sanchez, N. Poungvarin, A. Oliva, M. Vatta, J. Brugada, P. Brugada, J. A. Towbin, R. Dumaine, C. Pinero-Galvez, C. Antzelevitch, and R. Brugada, 'Phenotypic characterization of a large European family with Brugada syndrome displaying a sudden unexpected death syndrome mutation in SCN5A:,' J Cardiovasc Electrophysiol , vol. 15, pp. 64-69, Jan 2004. Evaluation Studies.
91. J. Brugada, P. Brugada, and R. Brugada, 'The syndrome of right bundle branch block ST segment elevation in V1 to V3 and sudden death-the Brugada syndrome,' Europace , vol. 1, pp. 156-166, Jul 1999.
92. P. Brugada and J. Brugada, 'Right bundle branch block, persistent ST segment elevation and sudden cardiac death: a distinct clinical and electrocardiographic syndrome. A multicenter report,' J Am Coll Cardiol , vol. 20, pp. 1391-1396, Nov 1992.
93. M. Bessette and S. Jacobson,'Torsade de Pointes,' eMedicine , vol. http://www.emedicine.com/emerg/topic596.htm, May 2006.
94. P. J. Schwartz and A. Malliani, 'Electrical alternation of the T-wave: clinical and experimental evidence of its relationship with the sympathetic nervous system and with the long Q-T syndrome,' Am Heart J , vol. 89, pp. 45-50, Jan 1975.
95. B. Surawicz and C. Fisch, 'Cardiac alternans: diverse mechanisms and clinical manifestations,' J Am Coll Cardiol , vol. 20, no. 2, pp. 483-499, 1992.
96. W. Shimizu and C. Antzelevitch, 'Cellular and ionic basis for T-wave alternans under long-QT conditions,' Circulation , vol. 99, pp. 1499-1507, Mar 1999.
97. R. L. Verrier, 'T-Wave Alternans and Risk Stratification for Sudden Cardiac Death, http://www.physionet.org/events/hrv-2006/verrier.pdf .'

98. B.-R. Choi and G. Salama,'Simultaneous maps of optical action potentials and calcium transients in guineapig hearts: mechanisms underlying concordant alternans,' J Physiol (Lond) , vol. 529, no. 1, pp. 171-188, 2000.
99. J. N. Cohn, D. G. Archibald, S. Ziesche, J. A. Franciosa, W. E. Harston, F. E. Tristani, W. B. Dunkman, W. Jacobs, G. S. Francis, and K. H. Flohr, 'Effect of vasodilator therapy on mortality in chronic congestive heart failure. Results of a Veterans Administration Cooperative Study,' N Engl J Med , vol. 314, pp. 15471552, Jun 1986. Clinical Trial.
100. S. Miyoshi, T. Miyazaki, K. Moritani, and S. Ogawa, 'Different responses of epicardium and endocardium to KATP channel modulators during regional ischemia,' Am J Physiol , vol. 271, pp. 140-147, Jul 1996.
101. A. G. Kleber, M. J. Janse, F. J. van Capelle, and D. Durrer, 'Mechanism and time course of S-T and T-Q segment changes during acute regional myocardial ischemia in the pig heart determined by extracellular and intracellular recordings,' Circ Res , vol. 42, pp. 603-613, May 1978.
102. S. G. Dilly and M. J. Lab, 'Electrophysiological alternans and restitution during acute regional ischaemia in myocardium of anaesthetized pig,' J Physiol , vol. 402, pp. 315-333, Aug 1988.
103. W. Zareba, A. Moss, S. le Cessie, and W. Hall, 'T wave alternans in idiopathic long QT syndrome,' J Am Coll Cardiol , vol. 23, no. 7, pp. 1541-1546, 1994.
104. S. B. Platt, J. M. Vijgen, P. Albrecht, G. F. Van Hare, M. D. Carlson, and D. S. Rosenbaum, 'Occult T wave alternans in long QT syndrome,' J Cardiovasc Electrophysiol , vol. 7, pp. 144-148, Feb 1996. Case Reports.
105. M. Takagi, A. Doi, K. Takeuchi, and J. Yoshikawa, 'Pilsicanide-induced marked T wave alternans and ventricular fibrillation in a patient with Brugada syndrome,' J Cardiovasc Electrophysiol , vol. 13, p. 837, Aug 2002. Case Reports.
106. M. Chinushi, T. Washizuka, H. Okumura, and Y. Aizawa,'Intravenous administration of class I antiarrhythmic drugs induced T wave alternans in a patient with Brugada syndrome,' J Cardiovasc Electrophysiol , vol. 12, pp. 493-495, Apr 2001. Case Reports.
107. T. Ikeda, H. Sakurada, K. Sakabe, T. Sakata, M. Takami, N. Tezuka, T. Nakae, M. Noro, Y. Enjoji, T. Tejima, K. Sugi, and T. Yamaguchi, 'Assessment of noninvasive markers in identifying patients at risk in the Brugada syndrome: insight into risk stratification,' J Am Coll Cardiol , vol. 37, pp. 1628-1634, May 2001.
108. B. D. Nearing and R. L. Verrier,'Tracking cardiac electrical instability by computing interlead heterogeneity of T-wave morphology,' J Appl Physiol , vol. 95, pp. 2265-2272, Dec 2003.
109. F. Dessertenne, '[Ventricular tachycardia with 2 variable opposing foci],' Arch Mal Coeur Vaiss , vol. 59, pp. 263-272, Feb 1966. Case Reports.
110. D. M. Roden, 'Acquired long QT syndromes and the risk of proarrhythmia,' J Cardiovasc Electrophysiol , vol. 11, pp. 938-940, Aug 2000.
111. J. Ben-David and D. P. Zipes, 'Torsades de pointes and proarrhythmia,' Lancet , vol. 341, pp. 1578-1582, Jun 1993.
112. N. el Sherif, E. B. Caref, H. Yin, and M. Restivo, 'The electrophysiological mechanism of ventricular arrhythmias in the long QT syndrome. Tridimensional mapping of activation and recovery patterns,' Circ Res , vol. 79, pp. 474-492, Sep 1996.
113. S. C. Verduyn, M. A. Vos, J. van der Zande, A. Kulcsar, and H. J. Wellens, 'Further observations to elucidate the role of interventricular dispersion of repolarization and early afterdepolarizations in the genesis of acquired torsade de pointes arrhythmias: a comparison between almokalant and d-sotalol using the dog as its own control,' J Am Coll Cardiol , vol. 30, pp. 1575-1584, Nov 1997.
114. C. Antzelevitch, Z. Q. Sun, Z. Q. Zhang, and G. X. Yan, 'Cellular and ionic mechanisms underlying erythromycin-induced long QT intervals and torsade de pointes,' J Am Coll Cardiol , vol. 28, pp. 18361848, Dec 1996.
115. W. Shimizu and C. Antzelevitch, 'Cellular Basis for the ECG Features of the LQT1 Form of the Long-QT Syndrome : Effects of ß-Adrenergic Agonists and Antagonists and Sodium Channel Blockers on Transmural Dispersion of Repolarization and Torsade de Pointes,' Circulation , vol. 98, no. 21, pp. 2314-2322, 1998.
116. W. Shimizu, T. Ohe, T. Kurita, M. Kawade, Y. Arakaki, N. Aihara, S. Kamakura, T. Kamiya, and K. Shimomura, 'Effects of verapamil and propranolol on early afterdepolarizations and ventricular arrhythmias induced by epinephrine in congenital long QT syndrome,' J Am Coll Cardiol , vol. 26, pp. 1299-1309, Nov 1995.

117. H. H. Tie, Cellular Mechanisms of QT prolongation and Proarrhythmia induced by non-antiarrhythmic drugs . University of New south wales: Doctor in Medicine thesis, 1 ed., 2002.
118. C. Antzelevitch and S. Sicouri, 'Clinical relevance of cardiac arrhythmias generated by afterdepolarizations. Role of M cells in the generation of U waves, triggered activity and torsade de pointes,' J Am Coll Cardiol , vol. 23, pp. 259-277, Jan 1994.
119. C. Luo and Y. Rudy,'A dynamic model of the cardiac ventricular action potential. II. Afterdepolarizations, triggered activity, and potentiation,' Circ Res , vol. 74, no. 6, pp. 1097-1113, 1994.
120. S. Sicouri and C. Antzelevitch, 'A subpopulation of cells with unique electrophysiological properties in the deep subepicardium of the canine ventricle. The M cell,' Circ Res , vol. 68, pp. 1729-1741, Jun 1991.
121. G. X. Yan, W. Shimizu, and C. Antzelevitch, 'Characteristics and distribution of M cells in arterially perfused canine left ventricular wedge preparations,' Circulation , vol. 98, pp. 1921-1927, Nov 1998.
122. D. K. Swanson and J. G. Webster,'A model for skin-electrode impedance,' Biomedical Electrode Technology , vol. 41, no. 3, pp. 117-28, 1974.
123. D. M. Krikler and P. V. Curry,'Torsade De Pointes, an atypical ventricular tachycardia,' Br Heart J , vol. 38, pp. 117-120, Feb 1976.
124. M. S. SPACH, R. C. BARR, J. W. HAVSTAD, and E. C. LONG,'Skin-Electrode Impedance and Its Effect on Recording Cardiac Potentials,' Circulation , vol. 34, no. 4, pp. 649-656, 1966.
125. R. D. Gatzke, 'The electrode: A measurement systems viewpoint,' Biomedical Electrode Technology , pp. 99116, 1974.
126. L. A. Geddes and L. E. Baker, Principles of Applied Biomedical Instrumentation . Wiley-Interscience, 3 ed., 1989.
127. O. Schmitt and J. Almasai, 'Electrode impedance and voltage offset as they effect efficacy and accuracy of vcg and ecg measurements,' Proceedings of the XIth International Vectorcardiography Symposium. , pp. 24553, 1970.
128. H. H. Barrett, 'Transducers for Biomedical Measurements: Principles and Applications by R. S. C. Cobbold. Reviewer R. S. C. Cobbold.,' Review of Scientific Instruments , vol. 46, pp. 1595-1596, Nov. 1975.
129. H. E. B. Pardee, 'Concerning The Electrodes Used In Electrocardiography,' Am J Physiol , vol. 44, no. 1, pp. 80-83, 1917.
130. 'http://upload.wikimedia.org/wikipedia/commons/1/15/Differencemplifier.png.'
131. 'http://www.biosemi.com.'
132. 'http://upload.wikimedia.org/wikipedia/commons/3/30/Opampinstrumentation.png.'
133. L. A. Geddes and L. E. Baker, 'The relationship between input impedance and electrode area in recording the Ecg,' Med Biol Eng , vol. 4, pp. 439-450, Sep 1966.
134. C. E. Kossmann, D. A. Brody, G. E. Burch, H. H. Hecht, F. D. Johnston, C. Kay, E. Lepeschkin, H. V. Pipberger, H. V. Pipberger, G. Baule, A. S. Berson, S. A. Briller, D. B. Geslowitz, L. G. Horan, and O. H. Schmitt, 'Recommendations for Standardization of Leads and of Specifications for Instruments in Electrocardiography and Vectorcardiography,' Circulation , vol. 35, no. 3, pp. 583-602, 1967.
135. 'http://www.neuroscan.com/.'
136. 'http://www.biosemi.com/faq/fileormat.htm.'
137. A. MettingVanRijn, A. Kuiper, T. Dankers, and C. Grimbergen, 'Low-cost active electrode improves the resolution in biopotentialrecordings,' in Engineering in Medicine and Biology Society, 1996. Bridging Disciplines for Biomedicine. Proceedings of the 18th Annual International Conference of the IEEE , vol. 1, (Amsterdam, Netherlands), pp. 101-102, 1996.
138. 'http://www.biosemi.com/activetwoullpecs.htm.'
139. C. Zywietz, '[On the information content of ECG lead systems (author's transl)],' Biomed Tech (Berl) , vol. 23, pp. 16-22, Jan 1978.
140. R. L. Lux, A. K. Evans, M. J. Burgess, R. F. Wyatt, and J. A. Abildskov, 'Redundancy reduction for improved display and analysis of body surface potential maps. I. Spatial compression,' Circ Res , vol. 49, pp. 186-196, Jul 1981.
141. M. B¨ achlin, Standard and Personalised Segmentation of ECG Data . Universitaet Karlsruhe: Diploma Thesis, 2006.
142. 'http://www.physionet.org/physiobank/database/mitdb/.'
143. 'http://en.wikipedia.org/wiki/Principalomponentsnalysis.'
144. J. E. Jackson, A User's Guide to Principal Components . John Wiley and Sons, Inc., 2003.

145. I. Jolliffe, Principal Component Analysis . Springer, 2 ed., 2002.
146. 'http://en.wikipedia.org/wiki/Butterworthilter.'
147. S. Mallat, A Wavelet Tour of Signal Processing, Second Edition (Wavelet Analysis Its Applications) . Elsevier, 2 ed., 1998.
148. R. M. Rangayyan, Biomedical Signal Analysis: A Case-Study Approach (IEEE Press Series on Biomedical Engineering) . Wiley-IEEE Press, 2001.
149. B. C. S., G. R. A., and G. H., Introduction to wavelets and wavelet transforms . 1997.
150. I. Daubechies, 'Orthogonal bases of compactly supported wavelets,' Comm. Pure Appl. Math. , vol. 41, pp. 909-996, 1988.
151. A. Haar, 'Zur theorie der orthogonalen funktionensysteme,' Mathematische Annalen, LXIX , pp. 331-371, 1910.
152. 'http://en.wikipedia.org/wiki/Image:Haaravelet.svg.'
153. G. Strang and T. Nguyen, Wavelets and Filter Banks . Wellesley College, 1996.
154. R. Coifman and D. Donoho, Translation invariant denoising . Technical Report 475, Dept. of Statistics, Stanford University, 1995.
155. D. L. Donoho and I. M. Johnstone, 'Adapting to Unknown Smoothness Via Wavelet Shrinkage,' Journal of the American Statistical Association , vol. 90, 1995.
156. R. Quian Quiroga and H. Garcia, 'Single-trial event-related potentials with wavelet denoising,' Clin Neurophysiol , vol. 114, pp. 376-390, Feb 2003.
157. C. R. Meyer and H. N. Keiser, 'Electrocardiogram baseline noise estimation and removal using cubic splines and state-space computation techniques,' Comput Biomed Res , vol. 10, pp. 459-470, Oct 1977.
158. J. A. Van Alste and T. S. Schilder, 'Removal of base-line wander and power-line interference from the ECG by an efficient FIR filter with a reduced number of taps,' IEEE Trans Biomed Eng , vol. 32, pp. 1052-1060, Dec 1985.
159. L. Sornmo, 'Time-varying filtering for removal of baseline wander in exercise ECGs,' in Computers in Cardiology 1991. Proceedings. , (Venice), pp. 145-148, 1991.
160. S. Pandit, 'ECG baseline drift removal through STFT,' in Engineering in Medicine and Biology Society, 1996. Bridging Disciplines for Biomedicine. Proceedings of the 18th Annual International Conference of the IEEE , vol. 4, (Amsterdam), pp. 1405-1406, 1996.
161. N. V. Thakor and Y. S. Zhu, 'Applications of adaptive filtering to ECG analysis: noise cancellation and arrhythmia detection,' IEEE Trans Biomed Eng , vol. 38, pp. 785-794, Aug 1991.
162. P. Laguna, R. Jane, and P. Caminal,'Adaptive filtering of ECG baseline wander,'in Engineering in Medicine and Biology Society, 1992. Vol.14. Proceedings of the Annual International Conference of the IEEE , vol. 2, pp. 508-509, 1992.
163. B. Mozaffary and M. A. Tinati, 'ECG Baseline Wander Elimination using Wavelet Packets,' Transactions On Engineering, Computing And Technology , pp. 1305-5313, 2004.
164. O. Pahlm and L. Sornmo, 'Software QRS detection in ambulatory monitoring-a review,' Med Biol Eng Comput , vol. 22, pp. 289-297, Jul 1984.
165. K
166. J. Pan and W. J. Tompkins,'A real-time qrs detection algorithm,' IEEE Trans. Biomed. Eng , vol. 32, no. 3, pp. 230-236, 1985.
167. A. Kyrkos, E. Giakoumakis, and G. Carayannis, 'Time recursive prediction techniques on QRS detection problem,' Proc. 9th Annu. Conf. IEEE Engineering in Medicine and Biology Society , pp. 1885-1886, 1987.
168. Q. Xue, Y. H. Hu, and W. J. Tompkins, 'Neural-network-based adaptive matched filtering for QRS detection,' IEEE Trans Biomed Eng , vol. 39, pp. 317-329, Apr 1992.
169. Y. H. Hu, W. J. Tompkins, J. L. Urrusti, and V. X. Afonso, 'Applications of artificial neural networks for ECG signal detection and classification,' J Electrocardiol , vol. 26 Suppl, pp. 66-73, 1993.
170. C. Li, C. Zheng, and C. Tai, 'Detection of ECG characteristic points using wavelet transforms,' IEEE Trans Biomed Eng , vol. 42, pp. 21-28, Jan 1995.
171. J. P. Martinez, R. Almeida, S. Olmos, A. P. Rocha, and P. Laguna, 'A wavelet-based ECG delineator: evaluation on standard databases,' IEEE Trans Biomed Eng , vol. 51, pp. 570-581, Apr 2004. Evaluation Studies.
172. S. Kadambe, R. Murray, and G. Boudreaux-Bartels, 'Wavelet transform-based QRS complex detector,' IEEE Transactions on Biomedical Engineering , vol. 46, no. 7, pp. 838-848, 1999.

173. A. Gutierrez, P. Hernandez, M. Lara, and S. Perez, 'A QRS detection algorithm based on haar wavelet,' in Computers in Cardiology 1998 , (Cleveland, OH, USA), pp. 353-356, 1998.
174. S. Abboud and D. Sadeh, 'The use of cross-correlation function for the alignment of ECG waveforms and rejection of extrasystoles,' Comput Biomed Res , vol. 17, pp. 258-266, Jun 1984.
175. S. L. Horowitz, 'A syntactic algorithm for peak detection in waveforms with applications to cardiography,' Commun. ACM , vol. 18, no. 5, pp. 281-285, 1975.
176. G. Belforte, R. De Mori, and F. Ferraris, 'A contribution to the automatic processing of electrocardiograms using syntactic methods,' IEEE Trans Biomed Eng , vol. 26, pp. 125-136, Mar 1979.
177. J. A. Vila, Y. Gang, J. M. Rodriguez Presedo, M. Fernandez-Delgado, S. Barro, and M. Malik, 'A new approach for TU complex characterization,' IEEE Trans Biomed Eng , vol. 47, pp. 764-772, Jun 2000.
178. P. Laguna, N. V. Thakor, P. Caminal, R. Jane, H. R. Yoon, A. Bayes de Luna, V. Marti, and J. Guindo, 'New algorithm for QT interval analysis in 24-hour Holter ECG: performance and applications,' Med Biol Eng Comput , vol. 28, pp. 67-73, Jan 1990.
179. W. Bystricky and A. Safer, 'Modelling t-end in holter ECGs by 2-layer perceptrons,' 2002 Computers in Cardiology , pp. 105-108, 2002.
180. N. Hughes and L. Tarassenko, 'Automated QT interval analysis with confidence measures,' in Computers in Cardiology, 2004 , pp. 765-768, 2004.
181. N. Hughes, L. Tarassenko, and S. Roberts, 'Markov models for automated ecg interval analysis,' 2004.
182. Q. Zhang, A. Illanes Manriquez, C. Medigue, Y. Papelier, and M. Sorine, 'Robust and efficient location of t-wave ends in electrocardiogram,' in Computers in Cardiology, 2005 , pp. 711-714, 2005.
183. M. E. Nygards and L. Sornmo, 'Delineation of the QRS complex using the envelope of the e.c.g,' Med Biol Eng Comput , vol. 21, pp. 538-547, Sep 1983.
184. A. S. Koeleman, H. H. Ros, and T. J. van den Akker, 'Beat-to-beat interval measurement in the electrocardiogram,' Med Biol Eng Comput , vol. 23, pp. 213-219, May 1985.
185. I. Duskalov, I. Dotsinsky, and I. Christov, 'Developments in ECG acquisition, preprocessing, parametermeasurement, and recording,' IEEE Engineering in Medicine and Biology Magazine , vol. 17, no. 2, pp. 50-58, 1998.
186. P. de Chazal and B. Celler, 'Automatic measurement of the QRS onset and offset in individual ECGleads,' in Engineering in Medicine and Biology Society, 1996. Bridging Disciplines for Biomedicine. Proceedings of the 18th Annual International Conference of the IEEE , vol. 4, (Amsterdam, Netherlands), pp. 1399-1400, 1996.
187. I. K. Daskalov and I. I. Christov, 'Electrocardiogram signal preprocessing for automatic detection of QRS boundaries,' Med Eng Phys , vol. 21, pp. 37-44, Jan 1999.
188. J. G. Kemmelings, A. C. Linnenbank, S. L. Muilwijk, A. SippensGroenewegen, A. Peper, and C. A. Grimbergen, 'Automatic QRS onset and offset detection for body surface QRS integral mapping of ventricular tachycardia,' IEEE Trans Biomed Eng , vol. 41, pp. 830-836, Sep 1994.
189. P. Strumillo, 'Nested median filtering for detecting t-wave offset in ECGs,' Electronics Letters , vol. 38, no. 14, pp. 682-683, 2002.
190. E. Soria-Olivas, M. Martinez-Sober, J. Calpe-Maravilla, J. F. Guerrero-Martinez, J. Chorro-Gasco, and J. Espi-Lopez, 'Application of adaptive signal processing for determining the limits of P and T waves in an ECG,' IEEE Trans Biomed Eng , vol. 45, pp. 1077-1080, Aug 1998.
191. H. Vullings, M. Verhaegen, and H. Verbruggen, 'Automated ECG segmentation with dynamic time warping,' in Engineering in Medicine and Biology Society, 1998. Proceedings of the 20th Annual International Conference of the IEEE , (Hong Kong, China), pp. 163-166, 1998.
192. M. Emdin, A. Taddei, M. Varanini, J. Marin Neto, C. Carpeggiani, Lapos, A. Abbate, and C. Marchesi, 'Compact representation of autonomic stimulation oncardiorespiratory signals by principal component analysis,' in Computers in Cardiology 1993. Proceedings. , (London, UK), pp. 157-160, Sept. 1993.
193. J. Presedo, E. Fernandez, J. Vila, and S. Barro, 'Cycles of ECG parameter evolution during ischemic episodes,' in Computers in Cardiology 1996 , (Indianapolis, IN, USA), pp. 489-492, Sept. 1996.
194. W. Sandham, D. Thomson, and D. Hamilton, 'ECG compression using artificial neural networks,' in Engineering in Medicine and Biology Society, 1995. IEEE 17th Annual Conference , vol. 1, (Montreal, Que., Canada), pp. 193-194, Sept. 1995.

195. Y. Nagasaka and A. Iwata, 'Performance evaluation of BP and PCA neural networks for ECG data compression,' in Neural Networks, 1993. IJCNN '93-Nagoya. Proceedings of 1993 International Joint Conference on , vol. 1, pp. 1003-1006, Oct. 1993.
196. H. Teodorescu and C. Bonciu,'Feedforward neural filter with learning in features space.preliminary results,' in Neuro-Fuzzy Systems, 1996. AT'96., International Symposium on , (Lausanne, Switzerland), pp. 17-24, Aug. 1996.
197. E. Costa and J. Moraes, 'QRS feature discrimination capability: quantitative and qualitativeanalysis,' in Computers in Cardiology 2000 , (Cambridge, MA, USA), pp. 399-402, 2000.
198. T. Stamkopoulos, K. Diamantaras, N. Maglaveras, and M. Strintzis, 'ECG analysis using nonlinear PCA neural networks for ischemiadetection,' Signal Processing, IEEE Transactions on [see also Acoustics, Speech, and Signal Processing, IEEE Transactions on] , vol. 46, pp. 3058-3067, Nov. 1998.
199. F. Vargas, D. Lettnin, M. de Castro, and M. Macarthy, 'Electrocardiogram pattern recognition by means of MLP network and PCA: a case study on equal amount of input signal types,' in Neural Networks, 2002. SBRN 2002. Proceedings. VII Brazilian Symposium on , pp. 200-205, 2002.
200. D. Newandee, S. Reisman, A. Bartels, and R. De Meersman, 'COPD severity classification using principal component and cluster analysis on HRV parameters,'in Bioengineering Conference, 2003 IEEE 29th Annual, Proceedings of , pp. 134-135, Mar. 2003.
201. Y. Wenyu, L. Gang, L. Ling, and Y. Qilian, 'ECG analysis based on PCA and SOM,' in Neural Networks and Signal Processing, 2003. Proceedings of the 2003 International Conference on , vol. 1, pp. 37-40, Dec. 2003.
202. P. M. Okin, R. B. Devereux, R. R. Fabsitz, E. T. Lee, J. M. Galloway, and B. V. Howard, 'Principal Component Analysis of the T Wave and Prediction of Cardiovascular Mortality in American Indians: The Strong Heart Study,' Circulation , vol. 105, no. 6, pp. 714-719, 2002.
203. S. Severi, S. Vecchietti, S. Cavalcanti, A. Santoro, and J. de Bie, 'Analysis of t wave complexity during arrhythmic phases caused byhemodialysis,' in Computers in Cardiology 2001 , (Rotterdam, Netherlands), pp. 637-640, 2001.
204. M. Zabel, B. Acar, T. Klingenheben, M. R. Franz, S. H. Hohnloser, and M. Malik,'Analysis of 12-lead t-wave morphology for risk stratification after myocardial infarction,' Circulation , vol. 102, no. 11, pp. 1252-1257, 2000.
205. P. M. Okin, R. B. Devereux, B. V. Howard, R. R. Fabsitz, E. T. Lee, and T. K. Welty, 'Assessment of QT interval and QT dispersion for prediction of all-cause and cardiovascular mortality in american indians: The strong heart study,' Circulation , vol. 101, pp. 61-66, Jan 2000.
206. M. Kesek, T. Jernberg, B. Lindahl, J. Xue, and A. Englund, 'Principal component analysis of the t wave in patients with chest pain and conduction disturbances,' Pacing Clin Electrophysiol , vol. 27, pp. 1378-1387, Oct 2004.
207. P. Laguna, R. Jane, O. Meste, P. W. Poon, P. Caminal, H. Rix, and N. V. Thakor, 'Adaptive filter for eventrelated bioelectric signals using an impulse correlated reference input: comparison with signal averaging techniques,' IEEE Trans Biomed Eng , vol. 39, pp. 1032-1044, Oct 1992.
208. A. Khawaja and O. D¨ ossel, 'Pca-based confidence measure for automatic ecg segmentation,' in BMT 2006, 'Biomedizinische Technik' CD Proceeding, ISSN 0939-4990 , 2006.
209. E. Laciar, R. Jane, and D. H. Brooks, 'Improved alignment method for noisy high-resolution ECG and Holter records using multiscale cross-correlation,' IEEE Trans Biomed Eng , vol. 50, pp. 344-353, Mar 2003. Evaluation Studies.
210. R. Jane, H. Rix, P. Caminal, and P. Laguna, 'Alignment methods for averaging of high-resolution cardiac signals: a comparative study of performance,' IEEE Trans Biomed Eng , vol. 38, pp. 571-579, Jun 1991.
211. R. R. Shah, 'Drug-induced QT dispersion: does it predict the risk of torsade de pointes?,' J Electrocardiol , vol. 38, pp. 10-18, Jan 2005.
212. S. Seitz, A. Khawaja, and O. D¨ ossel, 'Pca-based method for clustering t-waves,' in BMT 2006, 'Biomedizinische Technik' CD Proceeding, ISSN 0939-4990 , 2006.
213. D. Cuesta-Frau, J. C. Perez-Cortes, and G. Andreu-Garcia, 'Clustering of electrocardiograph signals in computer-aided Holter analysis,' Comput Methods Programs Biomed , vol. 72, pp. 179-196, Nov 2003.
214. D. Novak, D. Cueta-Frau, P. Mico Tormos, and L. Lhotska, 'Number of arrhythmia beats determination in holter electrocardiogram: how many clusters?,' in Engineering in Medicine and Biology Society, 2003. Proceedings of the 25th Annual International Conference of the IEEE , vol. 3, pp. 2845-2848, Sept. 2003.

215. S. Jankowski, A. Oreziak, A. Skorupski, H. Kowalski, Z. Szymanski, and E. Piatkowska-Janko, 'Computeraided morphological analysis of holter ECG recordings based on support vector learning system,' 2003 Computers in Cardiology , pp. 597-600, Sept. 2003.
216. Matlab 7, Statistics Toolbox . The Mathworks, 2005.
217. 'Electrocardigram,(ECG)-I, http://www.cs.wright.edu/ phe/EGR199/Lab/.'
218. I. The MathWork, Curve Fitting Toolbox User's Guide . The MathWork, Inc., 2005.

ISBN:  978-3-86644-132-3

ISSN:  1864-5933