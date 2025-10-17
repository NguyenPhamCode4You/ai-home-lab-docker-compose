# Video Transcription

## Summary
This document contains the transcription of the provided video file.

## Content

Transcription with Segment Timestamps:
[00:00 - 00:15] Hello, Jan. In this video, I want to discuss about how we want to handle the biofuel import from VFOS.

[00:15 - 00:30] What you are seeing in here is a typical good example of a bunkering event that we receive from VFOS. That if our vessel is receive biofuel, it will have this section available.

[00:30 - 00:45] will have like a biological part which is a fame mixed with the original fossil fuel and there are parameters available like the methane nitrous oxide and

[00:45 - 01:00] a parameter that we can use to calculate Vue EU but as you can see not all of the parameter is available so we have to preview some data with our default value if VFORCE doesn't provide for it.

[01:00 - 01:15] But anyway, we already discussed that we wanted to have a UI to display these parameters in our BunkerLot. So with this in mind, we have made an update on our estimate.

[01:15 - 01:30] That right now if you go into our estimate and on the bunker lot tab, you see that in the three dots over here, we have a build plan section for

[01:30 - 01:45] our bunker lot that you can click on and when you click on that you will our system will display the parameters that we have as a default value for our bunker lot

[01:45 - 02:00] parameter is important to be used to calculate for the build field and we use it according to the table that you provide for us as a default one in here

[02:00 - 02:15] We would see we have VOSFO and MGO available with these parameters. Biodiazo, FAME and the HVO is the two BIO plan part that we can have into our system.

[02:15 - 02:30] So here is the display value for VLSFO and if there's no plan you see it is 91 as the final W2W value. That this value will end up displaying in here when we use it.

[02:30 - 02:45] the view as a whole okay so if we have a plan available or if you wanted to change the plan here's how you can do it in here we have the view section that you can choose and then you can choose

[02:45 - 03:00] use a frame build path to be blended into our view example. And you can see this value is displayed for the frame value which is 16.

[03:00 - 03:15] something like this one okay and then there will be like a section that you can change the percentage of the flame by default would be 24 but

[03:15 - 03:30] if you can change it to 20, you see that the blended section will automatically calculate it. That you can change the percentage of the blended part over here. And also you can switch to

[03:30 - 03:45] another plane which is fine just like this one and the system automatically calculated so let's say we choose 20% of the frame to be plane and in here you can also directly change this value

[03:45 - 04:00] If you prefer to have it, like for example 5.9, the system will automatically calculate this value, just like this one.

[04:00 - 04:15] And if you wanted to revert it back to the default value, you can click on this button to bring the default value back. And the result of the plan when we click on OK.

[04:15 - 04:30] And then we click on Recalculate. On the View EU tab, you would see that when we use the view SFO, it will become this blended value. Yeah.

[04:30 - 04:45] Whenever there is a VLSFO, it will be used this planted value as you can see. But up until maybe this point, you see it become a different value. The reason for this VLSFO has a different value

[04:45 - 05:00] different value is because it already used up all of the first all of the first slot so the lot that contain the build part this one has already been used

[05:00 - 05:15] up and it start using the second lot and because the second lot doesn't have a plan so it will have this value and we also perform a weighting average to display the value

[05:15 - 05:30] that you see in here as the 86 as the final value we can also double check that if we change this the order of this bunker lot you can also

[05:30 - 05:45] see the changes and of course if you don't want it to have a plan anymore you can just go in here and by the frame there is a small delete button that you can click and then it will bring back

[05:45 - 06:00] the the lot to like a default fossil fuel state click on calculate on our fuel EU you will see our VOSFO now become 91 again every VOSFO

[06:00 - 06:15] of all we will come 91 again so with this component we will be able to map the value that VFORCE provides when we import the bunkering

[06:15 - 06:30] report from very first we will transform this data section into our into our data structure and also preview our default value into it to use it as a calculation for our view you and of course

[06:30 - 06:45] the operator, they can change the parameter available over here if they wanted to. And of course, this component also available on the voice part is exactly the same.

[06:45 - 07:00] So when we go into any of our voyages, in the bunker lot, there is also a bioplane part that we can also use that maybe I add week of fame, SVO.

[07:00 - 07:15] and then I use it as 30% length and then the expected value would be 69 then I click Calculate so the VOSFO, the first one will become 69

[07:15 - 07:30] the logic is there it share the same behavior from the estimate to the voyage so we can do like estimate to voyage transition easily and of course

[07:30 - 07:45] In the Vessel report, when there is a receiver report like this one, we also have a little eye icon over here that if we click on it, we will also display the same component.

[07:45 - 08:00] But for this section, we will display the value directly imported from VFOS. And of course, the operator can change or if they don't want it to change, we can also do that. And if the operator opts out,

[08:00 - 08:15] the receiver report this event will become a real lot on board and of course it will bring also the parameter of the bill field into the lot and thus the calculation

[08:15 - 08:29] for fuel eu will work so this is the update on the biofuel import from vefos if you have any idea to improve let us know thank you very much for your attention



---
*Generated using Whisper large v3 and processed automatically*
