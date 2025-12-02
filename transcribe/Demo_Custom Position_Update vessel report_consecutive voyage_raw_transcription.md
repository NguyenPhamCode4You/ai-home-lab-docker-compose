# Video Transcription

## Summary
This document contains the transcription of the provided video file.

## Content

Transcription with Segment Timestamps:
[00:00 - 00:20] Okay, so today I will demo to Christina a lot of things. So from our previous meeting, we have like a feedback on the vessel.

[00:19 - 00:39] the vessel report right in the rotation change and how if we delete a rotation in between then the vessel report how it would behave the second thing is to also improve here and there the validation on the vessel report and

[00:38 - 00:58] and the final thing is the the first draft on the consecutive voyage of which we will see how we wanted to insert a voyage in between yeah so i think i will start first with uh with the update on the vessel report first

[00:57 - 01:17] vessel report first. In here, I'm having data on my local host, so it would be a bit slower compared to the real system. So in here, we have a vessel that is coming from Bombay to

[01:16 - 01:36] Then I go to the report. There are some reporting coming up next. I can try to approve this one.

[01:35 - 01:55] and then I will try to change the direction of the noon report here so it is importing a bit so no new okay there's a lot of new report coming in

[01:54 - 02:14] But I think for to be easy, I will try to delete from here to here.

[02:13 - 02:33] ok approve these three reports so right now our last report we have a noon report coming from

[02:32 - 02:52] From back to Singapore, the drop is not consistent so might need to change a bit. This one should be like 741 maybe.

[02:51 - 03:11] Not yet. A hundred and... Five one? Five one. Okay. Eight. Some eight or nine, something like that.

[03:10 - 03:30] online something okay

[03:29 - 03:49] Look for this one again Okay So right now we have this Loon report And we open up our old vessel

[03:48 - 04:08] our old vessel or our old voyages here so in here it is reporting that we are coming from from back to singapore this new report over here from back to singapore and now let's say we don't want to go to singapore anymore we could insert something in between

[04:07 - 04:27] between and then we start reporting for it so maybe i will try to insert somewhere near singapore could be like already here okay

[04:26 - 04:46] Okay, then I save it. And I go back to vessel report. This is known as a port type passing, will it be working? Yeah, sorry. The passing will not work. Correct. So I need to change it to at least...

[04:45 - 05:05] to change it to at least some waiting and then put some day in it also could be okay what has happened now like you have not approved any report yet what is the eta true

[05:04 - 05:24] Is it the one from the latest new report or is it just from the distance from Phalan Bang to Vung Tau? What is the 29th? So in here, this 29 is calculated at the distance.

[05:23 - 05:43] the distance from Pompax to Vung Tau, not the current position of the of the vessel and then in here we can still keep Pompax to Singapore and we insert another vessel report

[05:42 - 06:02] And we see the second Vũng Tàu appear after the comeback. Actually, in here you can also change our noon report directly to Vũng Tàu, but it's fine to keep it here.

[06:01 - 06:21] Keep it here. So previous is pawn back and now I wanted to go to Vung Tau instead. I can also try to to select Vung Tau to Vung Tau but the system on the front end will try to correct it.

[06:20 - 06:40] So if we select Vung Tau, the next spot should be Singapore over here. And if we select Palmback, it will select the first spot at Vung Tau discharging. So it has some validation on the front end that

[06:39 - 06:59] that these two ports should be next to each other so if we choose for example we switch this one to Singapore and the next port should be Clang as the next of it and if we choose this one as Vung Tau it understand that the previous should be this one

[06:58 - 07:18] Okay, so I will insert the time of report, so maybe 27 of November 28, and I'm somewhere here.

[07:17 - 07:37] okay distant travel could possibly get 102

[07:36 - 07:56] Distance traveled to Vung Tau should be 111. I could do this one. Sorry, distance traveled is 28. Distance to go could be 121.

[07:55 - 08:15] okay need a bit of time to the approve button to appear okay and you go back to the voice screen and click on reload

[08:14 - 08:34] Okay, then I will see from Palm Park to Vung Tau, it has, oh, still doesn't have.

[08:33 - 08:53] maybe the distance I saw it try to sum up but we need to see it here so in here right the first departure we still say it is from Pompatou of the old Singapore and we already

[08:52 - 09:12] and we already um intra 4 we don't count for this one distance to go is 270 the first noon report we got data from veforce we already traveled 200 and the second noon report

[09:11 - 09:31] Now it's the hour manual importing. We travel for another 28 and we have like a 111 more. So I would expect the distance from Vung Tau, from Pombachia to the new Vung Tau should be the sum of them. So I would try to see if it's the same.

[09:30 - 09:50] try to see it is 200 plus with 28 plus with 111 so it is like three three something yeah three three three nine okay so it's it is correct

[09:49 - 10:09] is correct. So what I'm trying to say is that the moment we try to insert Vũng Tàu after Palmback and then we save the distance might not be correct but after the new report coming in from Palmback to be reported to Vũng Tàu and the

[10:08 - 10:28] and the new data coming in and it has been approved the logic will do the sum of the distance has been traveled from Bombach to the new place which is the new Vung Tau here and thus it will be correct again after we approve the second report and I can also

[10:27 - 10:47] I can also give a try this is the case that we insert an itinerary in between so we don't delete any itinerary but now if what would happen if we change directly the destination we don't go to

[10:46 - 11:06] We don't go to Singapore anymore and we also don't go to Singapore to fuel which I will go into the Bunker Order and delete the Bunker Order here. Deleting the Bunker Order and the itinerary only have one fuel

[11:05 - 11:25] one fueling so it would expect to delete also the itinerary oh existing vessel report I could not okay it doesn't allow me to delete

[11:24 - 11:44] But if I try to remove it here, could I? Save it. So if you're, oh, it's coming back. I just wanted to ask a few questions.

[11:43 - 12:03] I just wanted to ask, if you remove the bunker port, the bunker order also goes away? Yeah. Okay. Ah, the vice versa, you mean? I don't think the vice versa will work. Deleting the bunker order will also remove the F here.

[12:02 - 12:22] the f here but remove the f here might not might not remove the bunker order so we still also need to go to bunker lot and click on the bunker order and deleting it again yeah okay but anyway we have

[12:21 - 12:41] Anyway, we have a report. So I would expect to be able to delete this one but seems like there is some hiccup that still doesn't allow me to delete. And then I go back to my report. Can I ask one more question? I

[12:40 - 13:00] i'm not sure 100 if we really want to delete the fueling port when we delete the bunker order so just to keep it in the back of our mind if maybe we want to yeah but anyway if it has

[12:59 - 13:19] anyway if it has just the type f i think it could go away because if it has let's say loading and fueling you would not delete the port you would just delete the app yes correct correct and if there are multiple bunker order in the same fueling

[13:18 - 13:38] same fueling. Deleting one bunker order will not delete the entire itinerary. Okay so this is how it would look like if Vung Tau has been removed from the itinerary. Then there is like

[13:37 - 13:57] There is like a might get re-approved icon here, you don't have to re-approve but it has an orange icon so you can check on what is wrong. So all of these things doesn't have anything wrong but in here this one it got the Vung

[13:56 - 14:16] the Vung Tau has been removed so we needed to click on that and maybe manually select the next one as the Singapore again. If you manually select something else now will it also correct the previous port?

[14:15 - 14:35] Yeah, it will also try to correct the previous port. Yeah, and then maybe in here I can also show that if we make a wrong lag. So this null should not exist because it is still in the future. But for some reason,

[14:34 - 14:54] the data is like this and if we try to approve hmm so now in the itinerary has the vessel arrived in Khalifa? correct ok

[14:53 - 15:13] It should not arrive in the port in the future when we have not sailed from the other port. But then technically it should not be possible to even go there.

[15:12 - 15:32] I think because maybe we just we just submit the the noon report we are not submitting an arrived

[15:31 - 15:51] submitting an arrival report. So let's try to submit an arrival at Khalifa and then if I re-approve this one, yeah it's a suitable

[15:50 - 16:10] it should not be too far in the future but the noon report is still get approved this one i need to check yeah okay so anyway um there's still like a lot of hiccup regarding the changing

[16:09 - 16:29] the changing of void rotation in between so I might need some more time on it so maybe right now we will see another thing that got updated here is the custom position

[16:28 - 16:48] position how the custom position also interfere with the report so I will try to create an estimate a simple estimate first with the custom

[16:47 - 17:07] with a custom position or i can also go back to that void and remove the thing that i don't need let's see just to keep it simple and remove this one

[17:06 - 17:26] This one have loading and it just could not be okay this one seems okay and then if we wanted to add a custom position this is how we want to do it

[17:25 - 17:45] want to do it. Firstly, we click on the route to open the map. And then we can locate the position and right click. Click on Add Viewer Position. The system will add a P in here by default. And you see we have like

[17:44 - 18:04] See we have like a P with a coordinate. We can also directly change it here or we can drag it and get it recalculated just like a normal itinerary. Let it go back and forth to try to visit all of these locations.

[18:03 - 18:23] That's the first thing that we have an update on. And then by default, the custom position will have a P as the itinerary. I can click save on it and then I go to reporting.

[18:22 - 18:42] okay this is the void

[18:41 - 19:01] Now if we click on Add a New, the very first report that we wanted to make a departure on Labri to Kepple Good Hope

[19:00 - 19:20] So we have a library here. Oh, it doesn't refresh. I think it's all passing points in your schedule as well. Correct, correct. It's all passing points. So let's try to make this one as waiting. So we can make like a report that

[19:19 - 19:39] a report that completely ignores these two itineraries and I try to reload this page departure okay so it automatically insert waiting as the next one and we don't have

[19:38 - 19:58] we don't have the the passing in between anymore and so the departure is maybe too far away I can try to insert it from our November 14th

[19:57 - 20:17] and then arrival could be 30 November

[20:16 - 20:36] distance to go I will try to insert some big value over here and then BunkerLock I see that I have three lots in total

[20:35 - 20:55] This drop is bring over from the previous void, so it has like a current drop to be minus, but I try to change it here.

[20:54 - 21:14] 60 and 80 so this is the very first report of this voyage and then

[21:13 - 21:33] And then, I will try to approve this one. So, let's say this is our first report. We departure from LaPrix. We go directly to Vumru. And then, we have some...

[21:32 - 21:52] some time like this one and the drop is like this this is our previous uh voyage and after the first report approved it will get it will get the lot has been approved on board

[21:51 - 22:11] board but the the distance might not be true okay the import departure yeah because the departure it doesn't have a c report yet so

[22:10 - 22:30] yet so we still see that the distance in here because we report 1600 maybe I will try to increase in here the distance to go I report from LaPree to Vumro is

[22:29 - 22:49] is 1600 it might not be true might not be true because in reality the system shows that these two points may be located like 11,000 miles away but this one is the value that I got it inserted

[22:48 - 23:08] and we got like a warning distance threshold is too big but still on the voyage it got carryover and it got break into two parts the first part is some aircar related region and the aircar is like 51 so

[23:07 - 23:27] 1600 minus with the 51 here we got like the remaining would be the non-air carpet and this is how it it shows in the bunker tab that we don't have like a passing point in between but in here we still have

[23:26 - 23:46] have we still see that the passing point exists but maybe the my is not the my in here is not correct okay i can also try to show you if i change it to 2400 and or even maybe 10 000.

[23:45 - 24:05] Then I try to save and approve again.

[24:04 - 24:24] should have deployed this one to somewhere because running in local would mean a lot of slowdown so now the distance is more

[24:23 - 24:43] more reasonable. We are close to the real distance in here and thus the distance started to show up correctly. So what it tried to do is that the captain report 10,000 miles and it tried to calculate from La Prairie to this position

[24:42 - 25:02] to this position 1400 and from position to Cape Good Hope 4000. So it would expect to have another 4000 from this one to Vũng Rô. And 51 of these is actually Eka. So it will get reflected

[25:01 - 25:21] will get reflected in the bunker tab that you see 51 is still in ECA and the rest is the non-ECA and the MGL and VLSFO is calculated accordingly can you go back so that means if you go to overview tab

[25:20 - 25:40] That means the first two distances to the On-Sea and to the Cape of Good Hope are from Dataloi? Yes, correct. And the sum of this minus what the captain entered is then to Vũng Rô, right? Yeah. So basically, captain report from La Cri to Vũng Rô.

[25:39 - 25:59] Vũng Rô, 10,000 miles. So the system knows from here to here is 10,000 miles. But it doesn't have the distance from here to here and distance from here to here. So it needs to have a source of information. It goes to DataLoy and DataLoy returns. This is the value, this is the value.

[25:58 - 26:18] value so it automatically get the value that the captain report minus with these two to get this here well can you go to the root please because i'm a bit i'm wondering where this 50 uh seca eka miles come from

[26:17 - 26:37] from could be somewhere we don't know but only 51. would you expect some mekhamites credit somewhere from kpop good hope to bumbu we got this one i don't know

[26:36 - 26:56] maybe it's the e-commerce from the start port could that be right there yeah this is where they come from no this is high risk area no this is not okay

[26:55 - 27:15] I'm pretty sure this one comes from Dataloy somewhere. We just don't know exactly where it is on the road. But we just know that there are some 50 miles of aircraft in here, according to Dataloy.

[27:14 - 27:34] coming from c to here we we should look at the dataloy the blank dataloy response data okay so uh that's the first thing

[27:33 - 27:53] the first thing right then we can also try to insert a null report also the same from library to vumroo and this null report we are here we can even change this

[27:52 - 28:12] There's something wrong with this one, I cannot change the position anymore, which is kind of bad.

[28:11 - 28:31] 9 and then longitude I will go to main 40 ok and distance traveled may be 200

[28:30 - 28:50] 200 arrival time i could change it to something else december maybe now become one 21. distance to go maybe 28 000

[28:49 - 29:09] okay it doesn't get refreshed sorry click the need reload

[29:08 - 29:28] Spinning, oh, still got real data, ah, sorry, need to do one more.

[29:27 - 29:47] so i need to do it again 9 minus 40 time of report maybe this one will become

[29:46 - 30:06] 10th of December, we are 14th so 18th and the arrival time I would still keep the same. Then maybe I try to use the first

[30:05 - 30:25] the first 100 on VLS suppose and maybe use a bit on the first LSMGO things

[30:24 - 30:44] Okay I forgot to input the distance to go The system suggests like 1300, so maybe I will insert 14 and 10800 seems okay

[30:43 - 31:03] OK, OK, so we

[31:02 - 31:22] so we would expect to see the right now we are somewhere here according to the position we are coming near to here the bunker we shows that we already have an sc report of these two this one we burn two and this one we

[31:21 - 31:41] 2 and this one we burn 100 and the distance to go is uh the distance traveled is 1400 because this is the value we report and this is the distance to go ten thousand eight hundred we still see it ten thousand eight hundred in here

[31:40 - 32:00] And thus the VLSFO and LSMZOE is calculated accordingly. Can you go back to Bangkata? That was a bit. The RB at departure.

[31:59 - 32:19] Minus 1000 Because it's too much Okay, we just started with 200 We have still 100 on board, which is the value here For VOSFO, we currently only have 100

[32:18 - 32:38] have 100 and in order to go 10,000

[32:37 - 32:57] an arrival at Vumro you would expect us to pass this one completely but let's try need to have a refresh here and maybe arrival at Vumro and at the day

[32:56 - 33:16] I will change this to day 2 add 5 maybe we use all of this one only have 5 left

[33:15 - 33:35] and the distance already traveled is 10,000 doesn't look realistic

[33:34 - 33:54] okay okay so it bypass right now the this value is too big okay

[33:53 - 34:13] might need to double check again but yeah so departure we didn't travel anything the first noon report we travel 1400 and the arrival we try we travel 10 000 so in total

[34:12 - 34:32] so in total we travel 11,400 and it breaks down as this one the sum should be 11,400 The arrival distance traveled is also always from the last report, right? It does not concern the overall

[34:31 - 34:51] I'm not sure how it looks actually in the first report, to be honest. That's a good question. From the wrestling reports, it was like that. It was really the distance,

[34:50 - 35:10] distance reported from last departure but i am not sure if FOSS makes the difference in the arrival report or if they report the distance say like in every position report so this we need to verify

[35:09 - 35:29] we need to verify because if that is the case it should definitely not be summed up of course we could have it two way the first way is that what we are currently doing but the second way is that we completely don't show anything here

[35:28 - 35:48] show anything here and we just put 11 400 on the value on the itinerary that it got reported i think the logic to try to break it down also complicated a bit but we already have it here we can this is something

[35:47 - 36:07] This is something we can decide. Yeah, I mean, if it works properly, I think it is nice to have a breakdown, but I can also understand it is quite complicated. And it is, from my side also, rather just nice to have, to show the distance to the passing points.

[36:06 - 36:26] because there is only assumptions we only have the real figure for the next weighting or carbon related point these two values are just consumption

[36:25 - 36:45] Let me quickly show you what I can see.

[36:44 - 37:04] ..

[37:03 - 37:23] Now I'm going to change it a little bit up. Couldn't we see it also in VVMS for any existing world? Oh yeah, sure.

[37:22 - 37:42] I mean probably you would have noticed if it would be the total

[37:41 - 38:01] ..

[38:00 - 38:20] I forgot to start it. Whenever you stopped, I didn't really notice, but okay. Yeah, I think I stopped it during the time we talked about just the previous section. We might have lost it.

[38:19 - 38:39] okay so let's say we have this setup but maybe this setup is too complicated let's try to see if this vessel

[38:38 - 38:58] okay this look promising I will save it as grace okay this is the comments one the number one at Ginzu and then I go back I check on this one

[38:57 - 39:17] It's actually coming from Ginzo to the next one, Sedai. I think it looks okay. Then I go to Chartering. I try to create another voyage for this vessel. In here, I select the vessel.

[39:16 - 39:36] Vessel and then maybe I try to insert a shipment save it

[39:35 - 39:55] Save it and then create a new void for it. So this is our old void creation page. We can just click on confirm and then we create directly. But it would mean this one is not a consecutive void.

[39:54 - 40:14] a consecutive void but if I click on if this is a consecutive void then we can select which void it is consecutive to and by default we are creating void 3 so by default it will review the last one which is 2

[40:13 - 40:33] one which is 2. But I can actually insert void 1 at the first consecutive. But it would mean that this void number 2, when it got created, it will become the new number 2. And the old number 2 would become number 3. And it triggers the consecutive calculation

[40:32 - 40:52] the consecutive calculation so data from one will propagate to two and will propagate to three but i will show you by default this is how it will behave defaultly so if we click on i will show again for example so in here we can click on create voyage

[40:51 - 41:11] on create voyage and if you click on each consecutive two it will automatically preview the previous voyage so we are going away yeah it will be away meaning that this one is a non consecutive voyage

[41:10 - 41:30] way yeah probably you want to check it by default could be or what do you consider more i wonder what is more risky more realistic is also more risk more risky yeah um because i feel like that people will create voyages without the link right yeah or they create them with

[41:29 - 41:49] create them with link yeah i feel like this is less risky because now you see it's like and now oh yeah i want to remove i would rather do than i agree otherwise you can maybe just forget to check the box and then there is no really head to

[41:48 - 42:08] help to find out that you should do something if you want to want it not to be a consecutive i think the blue box and also the consecutive two will make you notice more that you shouldn't do this yeah so i think this could be the default setting yeah

[42:07 - 42:27] If we, by default, we are creating number 3 and it should be consecutive to 2 but actually you can make it become the new number 2 and make it consecutive to 1 but it will give a warning.

[42:26 - 42:46] you have chosen to create a consecutive that is not following the last void and doing so will update the void number so we click on create and we will proceed but I will try to this situation first we create a normal number tree first and

[42:45 - 43:05] okay so we have number three here and by the way ilka doesn't know yet two or one so i think she would like yeah i just i just wanted to first clear all of this with you

[43:04 - 43:24] this with you if it's okay and sounds promising and only then tell her yeah not that she's like in the mood i will get this for sure but then we know something is not working out yeah it's a good way to do it yeah okay so i will try to take the ring consecutive carefully it should work that

[43:23 - 43:43] should work that if we do any changes to void number one we will see it propagate to not void number two greenhole so if i click on this one number two should be from greenhole what is type this is a delivery and reading

[43:42 - 44:02] We still have a gap in here, we need to click refresh, now we can go to the next one and hopefully we see Sendai and stuff, next one, consecutive walk.

[44:01 - 44:21] Now I will show you we create the consecutive two. By the way we are here we can also mess around with the void number by having a three dot here and then change

[44:20 - 44:40] here and then change consecutive we can also do the same if we add it will give a confirmation you are about to change the consecutive void sequence doing so would update void number changing the void number of all of the void that go up to this one recalculating the consecutive data

[44:39 - 44:59] data and synchronizing all of the data changes to Business Central. This one I need to talk to them because changing this one would require him to also delete the old data of the void in Business Central and create a new one. So it's quite a big thing to do. We need to click on confirm.

[44:58 - 45:18] on confirm and then it will show that we are number three and we are being consecutive to two if i try to click on three it will scream because three cannot consecutive to three and we can change it to two which is the current set to situation we don't have confirmed but

[45:17 - 45:37] But if we change it to 1, it will make a warning and then we can confirm. But now I will demo the create of the devoid first. So let's say I'm still creating another estimate first.

[45:36 - 45:56] estimate for migration but right now the next estimate I don't make any shipment I may insert some some P and so

[45:55 - 46:15] and so waiting and then i say now we have a new estimate a void with no shipment and we can create a void e consecutive 2 by default would be 3 but now i can make

[46:14 - 46:34] but now I can make it consecutive to 1 or to 2. Let's try with 1 first. So we would expect this new one when it got created it will become number 2 and it changes the old 2 and 3 to 3 and 4.

[46:33 - 46:53] with w not going through the voyages would appear right the one we just observed 10 minutes ago yeah could be and i can at least would expect it to now happen as well so we see we see that this one is now number two

[46:52 - 47:12] We can go back to number 1, see it's Gwanzu, and it's making any changes to this one. We bring Gwanzu to the next.

[47:11 - 47:31] I mess around too much with the catching I need to refresh. Okay so we see that malgray here we got one two three

[47:30 - 47:50] one two three four this is the one and the next should be the one that no shipment one zoo being bring over with albrias and albrias bring over to number three sendai

[47:49 - 48:09] sendai and then number three bring sendai to santa so it uh no they also brought over correctly i think so it would bring over shipping okay so we can change queen hole

[48:08 - 48:28] Quinn Hall, 29, 23. Quinn Hall, 29, 23. And Albrecht, 10, 3, 4, 6. Albrecht, 10, 3, 4, 6. Can you not change the date, maybe?

[48:27 - 48:47] maybe if you now change the etd the departure of the last generation right here should be we can change it to 18. then we say this is a z okay

[48:46 - 49:06] Okay, so if we go to the next one, I think it doesn't bring over. Oh, it brings, but after a big refresh to clear out all of the caching.

[49:05 - 49:25] yeah there is some requirement to to catch the data in order to reduce the server workload but the catching here and there give confusing result because sometimes the front end just refuse to call the backend to get the new data so yeah that's it we save

[49:24 - 49:44] We save the data in your browser to make the system faster. Yeah, for those data you want to overwrite. Yeah, and then you're always in between. Okay, when do I always need it new and when not? This then needs to be fine-tuned. But I saw that the day has been bring over.

[49:43 - 50:03] bring over so if something is unlogic you would rather say refresh but just the normal refresh button in the browser is that overriding the cache or this one I don't know how she means this one this one was implemented

[50:02 - 50:22] this one was implemented by num right ah i didn't know this one but i think it should work it's implemented by num and it does just while here of course you do a hot refresh also getting front end from backend this one only does the api called sour backend without reloading the front end then

[50:21 - 50:41] front end. That's the idea of Num, that it would be like a faster refresh. You know, then you spare this 0.2 seconds for reloading the front end. That was his idea. Yeah, we can also try. So let's say I am number four and I want it to become

[50:40 - 51:00] it to become the new number 2. So it means that it will now become consecutive to number 1. You can do that by changing consecutive. So this component is available after we already created a void. So I click on this one and then I click on

[50:59 - 51:19] then I click on confirm now it become number two but the back and forth calculation took some time so we don't see the we don't see the itinerary got changed but if after some refresh we see that it now become

[51:18 - 51:38] Queen hole again because the number 1 is actually from Queen hole so this is number 2 The old 4 will now become Queen hole and the last of it is Santa so Santa should become for number 3

[51:37 - 51:57] for number three and ampere should become yeah for number four why this one is still number three you need to click on refresh okay so this one works yeah we can click on this one without clicking on this yeah so i think that's uh

[51:56 - 52:16] I think that shows how we can deal with the consecutive. When we create a void, we can already create directly where we want to insert a void. And after the void has been inserted, we can also rearrange the order.

[52:15 - 52:35] yeah but it still need to have some time in order for the recalculate consecutive to be fully calculated correctly so we might need to click on this one a few times to get the data yeah i'm thinking of having like

[52:34 - 52:54] having like a flag in the void that mark it as a warning if the consecutive in the background is running then we have that flag I wouldn't do I feel like this is not done on the this is from time to time done by postfix right guys who

[52:53 - 53:13] Guys who know what they do and who are not acting like crazy. Normal operators should not have the possibility, they should not even be shown. So it should be done by something who we expect to breathe in, breathe out and do it slowly and surely.

[53:12 - 53:32] but we can we should then discuss with them what they if they need this but for now i would not build anything just by assuming that they need okay yeah yeah but what i wanted to ask it here christina is that actually um nuna me discussed and we went for this to

[53:31 - 53:51] went for this to ensure that you guys would not lose voyage numbers so let's say another way of doing things could have been that if you or let's say if you now delete a voyage um you now delete the voyage four we yet discussed it that you probably would expect then voyage five

[53:50 - 54:10] then voyage five to become voyage four right you don't want to lose the voyage number even though it was planned and scheduled and anything right yes yeah okay yeah makes sense i think the the most realistic scenario is that you delete a voyage

[54:09 - 54:29] a voyage which is the last voyage anyway. So you don't have that problem so often that there is a next voyage scheduled which will automatically move back from the time. So it's not starting on the 1st of December but it's going to the 1st of November because

[54:28 - 54:48] because the monthly voyage in between is being deleted. It makes sense. I think that should be their behavior. But just to say from my side, I think it's 99% of the cases we are deleting a voyage which has not a next voyage yet.

[54:47 - 55:07] but then we could use it as a constraint right that you just can delete the last voyage and I mean you're good to reorder them anyway so you would reorder first make it the last voyage and then delete it or something like that yeah I think if that makes life easier for you I would have no problem if we do that because deleting

[55:06 - 55:26] because deleting a voyage in between I think is very unrealistic. Because also from the real life it would mean that the voyage you have planned for January 2026 immediately goes back into let's say December.

[55:25 - 55:45] say in December and usually our voyages are somehow related to a certain date when the cargo is ready somewhere and you cannot simply assume if I can lead a voyage in between I can carry on to the next voyage earlier because usually you would not have this flexibility with

[55:44 - 56:04] flexibility with the dates so i think it's more like okay i've planned a voyage for the maple grace in the future and it got canceled whatever so i will take it out and then i have not planned in the future after this voyage i guess so

[56:03 - 56:23] so it's mainly something that the last voyage has been deleted i think but deleting the middle could also be easily done christina okay i can also do that yeah okay okay i leave it up to you if you say it doesn't really make a difference for you then it's

[56:22 - 56:42] for you then it's nice because it's likely so we have one two is consecutive to one three it can send it four and four is consecutive to three even so deleting two would mean i just delete number two completely and then i go to three

[56:41 - 57:01] go to three make it consecutive to one and the logic would trigger now it become two and this one will become three so it's actually easy it's already there okay if it's already there i would like to keep it yeah okay because it does make sense if we do that and there is a void it makes sense to bring it forward

[57:00 - 57:20] So I can also make 2 consecutive to 4, meaning that we can change this 4 consecutive to 1, 4 consecutive to 2, we can also make 2 consecutive to 4, but doing so, it would mean that

[57:19 - 57:39] It would mean that we make this one, right? 3, 4, and 2. And thus it will make this one become new 2, become new 3, and become new 4. So make 2 consecutive to 4 doesn't make 2 become 5.

[57:38 - 57:58] Because 2 is the new 4, this is something I wanted to make it clear because it might feel confusing if we have that situation. So in here, let's say we are at number 2 and I want to change it.

[57:57 - 58:17] Change it to now become consecutive to the last one. To 4. But it doesn't become 5. It actually become the new 4. And the 4 will become the 3. Yeah, that makes sense. There should not be a gap, I would say. And if I click on refresh, it now become Sendai.

[58:16 - 58:36] Sendai yeah because number three here click on refresh yeah Sendai and then number two the new number two click on refresh yeah okay so that is

[58:35 - 58:55] so that is uh one thing we can do and uh okay i think another thing that we need to discuss is the non-consecutive how it would behave so in the voyage when we create by default it will have like a checkbox of consecutive

[58:54 - 59:14] for consecutive right but if we insert a void in between maybe but that is not consecutive then how it would interfere with the logic so let's say we have one consecutive to two consecutive to three already

[59:13 - 59:33] But now we want it to make a 4, consecutive to 4 that is not consecutive. Then, would it mean this one, 4 without a link? And then we create number 5, which is consecutive to 4.

[59:32 - 59:52] consecutive to 4. Is that possible? And if we're doing so, we don't have the consecutive of 4. So updating 1 will always update 2 and update 3. But it stops at 4 and thus it doesn't go to 5. Or it should jump 4 and go to

[59:51 - 60:11] four and go to five, I don't know yet. So how we would let this guy interfere with the logic? Should we jump or should we completely disconnect the value here? I think we have to disconnect. We have to disconnect. Yeah, so

[60:10 - 60:30] So from my understanding, a non-consecutive voyage can only happen if you terminate the contract somehow in between. I mean, the question is what happens with the vessel between 3 and 4.

[60:29 - 60:49] I mean, then normally, yeah, maybe we would also need Jan's input here, Jan Pauli's input, because he maybe knows more when this happens. But from my understanding, we, it is more of, we re-deliver the ship,

[60:48 - 61:08] the ship to the owner after voyage three and then maybe we get her back at four at a later stage not directly after three and then we can never make a connection from five to three so I think

[61:07 - 61:27] So I think there will be a cut in between 3 and 4. And 5 will thereafter be able to be consecutive to 4. Yes, like you draw it, but not 5 to 3. There will be like a cut and then you can also not play around anymore

[61:26 - 61:46] anymore with the order between five you cannot make consecutive to two I would say so I think you have a set of one two three you can switch around you have five six seven four five six something like that they will be

[61:45 - 62:05] not connected anymore i think yeah but uh i think my logic would still be allow the five to be consecutive to two even though it was created to be consecutive to four it would behave like this so it would put five to next it to

[62:04 - 62:24] 2 and then 5 and then 3 and then number 4 disconnected and then it changed to the new 3 changed this one to the new 4 and changed this one to the new 5 Is this okay? Or should we completely avoid

[62:23 - 62:43] avoid bringing fire to here because there is a disconnect here or should this one be okay this one is on already there the logic is there first one will be very complicated yeah it's the the first one we need to think about what do we in this uh pop-up what do we pre-fill into

[62:42 - 63:02] pre-filled into this drop-down this is what we need to think about because of course one day that's I mean what is now the rule for the options being shown in this drop-down that just all voyages or do you already filter by the status or filter by two things

[63:01 - 63:21] is consecutive to true for a number bigger or equal to the current commencing and the status equal to schedule

[63:20 - 63:40] second i think we misunderstood one another yeah i mean this one like the options in here yeah they are filtered by this yeah this so also vessel id

[63:39 - 63:59] I did equal to the current vessel so these are the voyage of this vessel only and the voyage number of all of these are bigger than the current commencing which is number 1, so it shows 1, 2, 3, 4 and all of them are like scheduled status so do you have a

[63:58 - 64:18] do you have a filter on the status of the voyage so because at the moment i mean my status is that i can run a voyage which is scheduled and completed it never really has to

[64:17 - 64:37] I mean, changing it to commence doesn't make a difference at the end for me. Does it make a difference for this rule, the status of the voyage? Yeah, I understand. Yeah, I mean, if one was scheduled as well,

[64:36 - 64:56] as well you could also put this voyage consecutive to one anyway so i think there's not really a difference in my question at the moment but there should not be two commences at the same time right so if i just should not but at the moment i think i couldn't cancel change the

[64:55 - 65:15] can still change the status of 1 and 2 to commence? Yes, I think you can do so. Now it would mess up. I mean, actually, if you say it would mess up this, that's okay, because there should not be 2 commence voyages of the same vessel.

[65:14 - 65:34] Couldn't you just put all the voyages which are either commenced or scheduled and that's it? Commenced, scheduled and completed. But the completed without... Yeah, you could also put it after a completed voyage. But just one completed, right? So it could be all commenced...

[65:33 - 65:53] all commands will be only one all scheduled okay but if you have a commands then it cannot be the completed one okay only if you don't have a commands then you want the last completed one in here as well i would try to find the last command or command

[65:52 - 66:12] command or complete as the start and then find every any void afterwards after it okay but after it will be hard if you have another non-consecutive chain right yeah because now there's a disconnect here

[66:11 - 66:31] There's a disconnect here, but actually the new one coming to the PHY can also be consecutive to 4 So I don't think we could limit down, we can also show 1, 2, 3, 4 and then because the PHY can be consecutive to any of this

[66:30 - 66:50] is yeah so actually still the rule was to hold true right just the last commenced or completed and all scheduled ones no matter if it's from this chain or this chain only if we click on the four the four

[66:49 - 67:09] the four is being created as a non-consecutive at the start but then if we wanted to make it consecutive again i don't know if we if we do that then we can also make use of this button change consecutive and then just make it now the four have a consecutive two three and then and

[67:08 - 67:28] and then it becomes consecutive again. She can easily do. But this one I think we need more polish to see how it works out. To me it feels risky, I have to admit. Risky? There's a lot that can go wrong. And what would you expect the opening position?

[67:27 - 67:47] I expect the opening position then to become... I think in real world that a voyage which used to be consecutive is then considered no more consecutive. Does that happen? Not really, right? I don't think so.

[67:46 - 68:06] we need to polish what we have and also polish the reporting instead first but maybe we can make this yeah just the pre-filling of this what we just discussed either

[68:05 - 68:25] either commands or last completed and all scheduled no matter from which from which consecutive string and then the your logic would work for all of those right yeah

[68:24 - 68:44] mm-hmm that one we can implement to see how it turns out we can always go back and update when the user see it is not it is not okay then we can change yeah i just wonder if we should show here that one

[68:43 - 69:03] show here that one maybe if one is not consecutive if we want to show it in any way but this is then fine-tuned but at least christina sees like the it's not about finished feature but the way we would now build it and i feel like it's it's fitting right yeah

[69:02 - 69:22] One more thing is that the consecutive logic would mess up if there is a canceled void in between. But hopefully with the delete void, we don't need to have a void at the cancel status more, right, Christina?

[69:21 - 69:41] Yes, I think a cancelled voyage does not have to be in the system in mind. To me it's also very very risky. Because you will have ports in the cancelled voyage which are never be called. So they should never be in the itinerary or anything.

[69:40 - 70:00] anything so yeah and which voyage number does the cancel voyage have because we actually want to have a consecutive running voyage number system so let's say i cancel voyage 2 it should make voyage 3

[69:59 - 70:19] voyage 3 become voyage 2. so i mean there are of course things which come to my mind which are useful to show a cancelled voyage like i can still go into the voyage and maybe i have to send an invoice to the client

[70:18 - 70:38] to the client because the client didn't have the cargo ready in time so then we say okay then we have to cancel the contract because we cannot load your cargo it's not being there so we get money from you and that would be on the cancelled voyage but this is nothing we have now. So it's more like a cancelled itinerary I think.

[70:37 - 70:57] itinerary item or I mean you probably could document it somehow with the shipment then or with the estimate of the shipment or so that would concern one leg within a voyage it can be both, it can be a complete

[70:56 - 71:16] can be a complete voyage on its own. Let's say voyage number two from Ras Laffan to La Brea was 200 containers and now while we are still in voyage one we learned that the containers will not be ready, they will not even have to be transported anymore, so we will cancel

[71:15 - 71:35] So we will cancel the contract and then we will not go to any of these calls anymore. And the whole voyage would have to be deleted. So and then I just said there is one advantage to have a canceled view, canceled voyage.

[71:34 - 71:54] We could still see what was planned on the ship and maybe even we have some income for that because the customer has to pay BBC for that we have planned to go there and we have now maybe two days before we start the voyage.

[71:53 - 72:13] He starts a voyage. He says, okay, I'm sorry, you cannot come anymore. And then we have the situation, the ship is unemployed and we have costs. And that is the reason why we are able to charge some costs to the customer in that case. But from my point of view, we

[72:12 - 72:32] we don't need the cancelled voyage to remain in the system as cancelled, from my point of view we delete it reports are gone and then if we really have some income for that we put it on a different voyage, that's how I know it from now, so I think it should

[72:31 - 72:51] so i think it should normally not be in the system anymore okay the estimate can be there for sure it remains it is in the past but in the voyage doesn't have to be there okay and if we cancel all the itinerary items the question is not if we have to delete

[72:50 - 73:10] we have to delete the void because it will remain just the itinerary changes so that's what i think then i think it's safe for for the first implementation

[73:09 - 73:29] first implementation so do you already have the possibility to delete for example voice number 4 i didn't do the delete for it yet okay didn't do it my next step but christina you also would say that it would be

[73:28 - 73:48] it would be the way cleaner way to first make this voyage like naked delete anything any off fires any thing like this before or put it elsewhere to make sure it's not gone yes me being alone this week i would say this is my preferred

[73:47 - 74:07] My preferred option to do that, to delete a voyage, where there are already things in the voyage, like you say, an off-wire, or let's say port cost, or other invoices,

[74:06 - 74:26] It forces the user to have a look at each of the items before simply deleting everything. They would auto delete all of these entries, which I think is not good. So either you want to shift them to other voyages, then you should do all of this first.

[74:25 - 74:45] Yes, or deleted but on purpose, I would say. So then we need to think about that the voyage should not have any, ideally not any shipments, not any laytimes, not any off-hires, and then we need to think a bit with num as well.

[74:44 - 75:04] with Nam as well, concerning invoice perspective. But from operational view, for me, it's that late times off-hires or late times TC claims and shipments. I couldn't think of anything else. Nam said that only no invoice had been created for the scheduled

[75:03 - 75:23] for the scheduled voyage yet just the data on the business central some master data related to the voyage information but that one he can easily delete

[75:22 - 75:42] Okay, so my next step is to work on delete voyage and also to, yeah, what did I just remember? The caching was still a bit problematic, right? Yeah. So maybe we can really...

[75:41 - 76:01] Maybe we can really use this from NAMM, so it really feels a lot faster, right? Maybe we can just always, when we click here, programmatically call this guy. Eventually we will need to call that guy a lot of times.

[76:00 - 76:20] and we defeat the purpose of having the catch yeah yeah but thank you it's messy hard to tell i mean you're yeah but you're right doing it all the time because just once a week somebody changes the order of voice

[76:19 - 76:39] the order of voyages is also not nice, right? If you're insecure, we don't do anything and we await. I leave it to you. I will try to improve to remove the cache where I know it should be removed.

[76:38 - 76:58] should be removed but don't spend like i feel like that it could easily get in a rabbit hole with this one right i mean if then it's the case hey for this voyage we know there's been a lot of changes there's been um one voyage being set before another next one then okay for now the user

[76:57 - 77:17] okay, for now the user should refresh the voyages. I think that's reasonable. It doesn't happen too often, right? So let's not build something that adds more complexity for the 99% of all other cases. Yeah.

[77:16 - 77:36] That's the nice to have thing right? So next thing on the list is the Elite Voyage. And then there are more again for the non-consecutive one.

[77:35 - 77:55] even before that i needed to revise on the itinerary of the vessel report during the demo it still got a bit messy then i think the

[77:54 - 78:14] I think the non-L and D itinerary items being passed through the consecutive for each chain consecutive one change allow the non-L and D to be passed into the consecutive or non-L and D but just actually it's just W and R

[78:13 - 78:33] just w and r right it's neither i it's neither p it's l d w or r if you write down non l and d i wonder if it also would allow to do this with p or i or we just allow what do you think is there any risks

[78:32 - 78:52] Is there any risk, you see, for allowing a P, if you have a P as the last one? I mean, a P can actually not really be the last one, I think, because the P is in the middle of two cones. The important reason is the P cannot have an arrival report.

[78:51 - 79:11] and the last item and the first item need reports so it cannot be p just for sure but also a canal passage it doesn't really make sense i mean it could happen but it

[79:10 - 79:30] happen, but again, it would rather be only if I, let's say, redeliver a ship somewhere because the voyage normally doesn't end at a canal, unless I discharge something at the Panama Canal, but then I could still call it the D. So I think also the I would not be

[79:29 - 79:49] not be the last i think we should explicitly just do ld w and r yeah l d w and r to be passed yeah okay okay i'm sorry but this concerns voice charter what about time charter what about the re-delivery as well right yes

[79:48 - 80:08] Yes. The Zed. That is you, yeah. The Zed can be the last. Needs to be the Zed, right? Not necessarily, because there are voyages, which, let's say, my voyage started at Antwerp, because the last voyage ended there.

[80:07 - 80:27] I discharged cargo in Antwerp, so that is always the point where the voyage ends, when the last cargo is off, and then I fixed a time charter contract with someone who only wants the vessel in Hamburg. So the lag between Antwerp and Hamburg is in the

[80:26 - 80:46] is in the new voyage, but it is not the why, which is the delivery, at the beginning. Because I will have a passage before this time-charter related function. So the same, I'm not sure, can it happen?

[80:45 - 81:05] Can it happen that the voyage ends not with a Z but after? But usually that would mean the voyage ends with a Z and the passage from where the chartreuse

[81:04 - 81:24] gave the vessel back to BBC, normally should end the time travel voyage and then travelling again and it would be coming back to the beginning what I said, the example Antwerp to Hamburg, this passage would be the new voyage. So technically voyage should always end with C.

[81:23 - 81:43] But if we allow W to be dragged over anyway, it should be no problem. The W is the solution for most things, right? Yes. Also, if you bandhas, then somewhere to reposition. Yeah, I think so. That's actually a good point.

[81:42 - 82:02] Do you know, Nguyen, there's this T port on Estimate? I also don't get the word. T? T, yeah, Terminating. There's C for Commencing, and in Estimate you can also do a T for Terminating. I just wonder...

[82:01 - 82:21] I just wonder how the T is copied over to Voyage I don't know right now but okay I think the T usually is when the time shatter ends and if you have an I'm mostly off

[82:20 - 82:40] when i was the option to mark a check box which says last time charter in voyage so when you activate this and you end the voyage by approving the last departure report the status of the

[82:39 - 82:59] the status of this part will not be d for departed but it will or s or what it is but it will be t because then the system knows this is the end of the voyage and also the time chart yeah we have an estimate we have t that

[82:58 - 83:18] that always at the end of an itinerary it will insert this port to communicate that no matter what we do in this voyage no matter what cargoes we do in the end we always want a ballast to this position that's the idea and i currently am not not sure how we transport

[83:17 - 83:37] we transport this T port from estimate to voyage. Probably we want to make it a W.

[83:36 - 83:56] terminating is confusing in this regard yeah but for sure it was considering voyage charters okay but i can have a look into this

[83:55 - 84:15] and maybe we want to look at this eckermals buggy behavior or maybe it's also just dataloy giving us this data but i think you can try we can try with the

[84:14 - 84:34] we can try with the um distance tool that value probably coming from that alloy this is a distance tool

[84:33 - 84:53] Just LA and then space.

[84:52 - 85:12] L A and then it's B R and now it's L M and one go even have bigger

[85:11 - 85:31] even have bigger that makes sense because it's go to Suez it doesn't go to yeah but mediterranean is probably already maybe they added mediterranean as and then yeah for sure i mean there's no

[85:30 - 85:50] I mean, there's no other explanation, right? Dataloi seemed to have added Mediterranean already as IKAR to their... This is an important note for us. It is not IKAR yet, right? Just from the first of... Well, the Mediterranean is since this year, May. Ah, May. Yeah, right. Okay.

[85:49 - 86:09] May of next year or this year? May of this year. I was mistaken. But I didn't see any egg. No, I'm sure that... Ah, it has. Yeah, it has.

[86:08 - 86:28] Okay, but where were these 50 coming from? Let's check again on where the 50 is. Okay, but we can check this on our own, no need for...

[86:27 - 86:47] no need for no need to waste time here

[86:46 - 87:06] I think this also was more than enough information, right? Even if there is more, I don't think that... Show Christina a bit on this one, this final thing.

[87:05 - 87:25] final thing that I saw that you guys see the undo arrival and undo departure yes so it's basically that for some time we also want to unblock this field to be able to edit again and that is the reason I make an undo so let's say we want

[87:24 - 87:44] so let's say we wanted to change the arrival we click on undo uh we want to change departure and then we click on undo departure we confirm and then we can change the departure time again maybe like this one

[87:43 - 88:03] But doing so, meaning that we might need to re-approve the report. Because the departure is blocked, meaning that the departure report has been approved before. And because we undo it, we might need to...

[88:02 - 88:22] double check and re-approve all of these. Maybe just this one but I need it to to clean out this one a bit. But anyway we can take a look at the data and then make some change and then re-approve again. There is a button to quickly re-approve it.

[88:21 - 88:41] without needing to we can just make a say and then say and re-approve or we can directly go and re-approve it in here i check the import again and that's it i think another thing is that we can also for some time

[88:40 - 89:00] that the vessel mistakenly jumped from the sun and arrived to Palmbeck, we already see it at that time we might want it to un-arrived Palmbeck directly or we wanted to bring back the vessel to some some old place so let's say we wanted

[88:59 - 89:19] let's say we wanted to bring it back to here. We can undo birth. Undo birth will undo both the birth and departure. And undo arrival will also undo arrival birth and departure. We can undo a pass.

[89:18 - 89:38] to jump back the vessel and then we can be able to change anything in the future and of course the report that has been affected will also be marked as orange that we might want to check again

[89:37 - 89:57] again. This report is affected because we changed the status of everything in between here. We might want to take a look and then re-approve all of them again. So I think this

[89:56 - 90:16] think this one i wanted to show but i also don't know what it would need to be behave exactly so i know that there's a case that we already got this one block but we wanted to unblock it but after we unblock we make changes should

[90:15 - 90:35] should it affect the report or should we go into the report and approve again kind of like back and forward it is not clear enough to me yet so i'm not sure if i understand the confusion completely but you

[90:34 - 90:54] you say like in the example i will the vessel has arrived birthed and departed so then i will say so the field will be white again and i can change with changes but in order to depart again

[90:53 - 91:13] again from Mazan, I need to approve the report, right? Otherwise I cannot simply say, okay, I changed the 12th November to the 13th in the schedule, okay, but in order to continue in the voyage, I need to take the report, right? Yeah, correct, correct. So is there

[91:12 - 91:32] Is there another question? I'm not sure, because I think from my side, I understand the question, do we need to do the report to correct whatever we want to have? And I would say, yes, I can do it manually, temporarily, as long as I don't want

[91:31 - 91:51] I don't want the vessel to say from the port, but finally I have to use the departure report or the arrival or the berthing report to log it in again. Yeah, correct. So right now the data flow is only one way from vessel report.

[91:50 - 92:10] from vessel report to the void updating the void here doesn't affect the vessel report already value in there i think that is good okay yeah i think it makes sense to only have one way and not go back to the report all the time if

[92:09 - 92:29] If I want to make changes, I have to manually change the report and approve it. And then we send the information through the itinerary again. But I would rather not think that it's necessary to make changes in the itinerary and update the report.

[92:28 - 92:48] updates and reports. It's from my side not necessary. Then I think it's safe for the logic. Do you update this instructed with the reports? You do? Okay, not needed.

[92:47 - 93:07] not needed shouldn't be done but we could this one you mean the small one yeah the small one i think i don't i don't make the small one here mika already asked that this value he input manually and this one should go to the report

[93:06 - 93:26] to the report not the other way around that the value in the report propagate back to here the small one what is the value i don't know this misunderstanding where is it coming from the instructions the instruct the ens the smaller one is

[93:25 - 93:45] one is whatever the operator input and this should stay yeah this should stay forever because it's manually changes

[93:44 - 94:04] speeds in between the ports are so different because i i don't know if you have put all the different but 15.7 16 13.4 that doesn't really look like a manual entry this one yeah in between

[94:03 - 94:23] the gray and the instructor speed between all the ports is always different 13 14.8 15.7 16 so it doesn't really look like a manual entry somebody has not gone in between and put all these different numbers right yeah

[94:22 - 94:42] So I was wondering where it comes from. Also no idea. So you are not knowing about your logic overwriting this piece of data, right?

[94:41 - 95:01] I just know that this value should go into the report. I also don't get why it should go into the report. Mika already said it last time that he wanted to have... As the comparison value you mean?

[95:00 - 95:20] Yeah, it's here. So this is the speed to go reported by vessel. This is the instructed speed. Yeah, okay, this makes sense. This value coming from the outside. Yeah. Okay, so it goes into the report data, it's just displayed.

[95:19 - 95:39] data it's just displayed yeah okay but uh updating here we should not should not change the the value there yeah yeah so we need to consider this instructed speed is just as a note it's just a note for each itinerary item what

[95:38 - 95:58] what used to be the instructed speed. But at some point it gets overridden. I still don't really understand why it gets overridden. It needs to be some bug somewhere. Because I would expect it should be like a constant figure through all the

[95:57 - 96:17] then okay i think i can try re-approve it again to see if this one got override the 13 value i could put it into 19. okay let's see can you refresh

[96:16 - 96:36] can you refresh once just to be sure okay i think let me go to report

[96:35 - 96:55] Too slow. Fifty-three.

[96:54 - 97:14] Okay, it might take some time.

[97:13 - 97:33] While we wait for this one, I will try to formulate what my question just previously for Christina is that so if we got it blocked.

[97:32 - 97:52] if we got it blocked it here meaning that an old departure has been approved for this one to get it blocked and then for some reason we want to make changes then we can also do the undo departure to get it unlocked again and then we make changes to it and say if it is okay

[97:51 - 98:11] and save it is okay but the change directly here will not go to the departure report instead we wouldn't if this one need to be blocked again we would need to go to the departure report make menu adjustment and re-approve then it will block okay then it's actually already that way

[98:10 - 98:30] Another thing, it is also possible in this stage when the departure Ulzan is already blocked, I go in the departure Ulzan report, make a change, and just re-approve, I can also overwrite the departure time, right? Should be.

[98:29 - 98:49] should be okay should be even without opening it in between should be yeah like we can try that now also let's wait a bit more

[98:48 - 99:08] We change it 19 at Marzahn. So if I click on refresh this one, it blocked Marzahn and this one become 19 again. But birthing and departure report for Marzahn are not yet done, right? Let's see.

[99:07 - 99:27] Let's see. Let's see when this one gets locked. In reality, Christina, would you do this or would you just consider arrival, birthing, unbirthing, departure?

[99:26 - 99:46] unbirthing departure report would you even re-approve all the import reports because they anyway make one another obsolete right yeah i think normally we would not go through all the input reports again because there's no information which is

[99:45 - 100:05] which is being saved somewhere in the background, right? I mean, there is no distances from somewhere, like an intra-distance we would normally use, but it's not in port-to-port, so I think there is nothing from my side

[100:04 - 100:24] which needs to be re-approved then. Also the departure time is not updated, so... Yeah, even if it is once there's the departure report, that's the one which decides, right? But you would not need the undo arrival in any circumstance, right?

[100:23 - 100:43] understand this right just undo departure because i would say undo arrival would affect the input possibly well i mean let's say no matter if you do undo arrival or undo departure say the imports you have arrival report here

[100:42 - 101:02] here, we have departure report here birth, unbirth, ok and then arrival birth and there is a whole lot of import reports right here and now say you do something with this, actually now Christina would go back here, she would ignore or I would assume

[101:01 - 101:21] or i would assume she would ignore them and really just go let's say to this one we approve to this one we approve ignore all of these just keep them unapproved in the system go to this one we approve go to this one we approve and do that for the two or three port calls that got effective

[101:20 - 101:40] the only thing which i just think about is maybe um if i want to change something with the report but the lesson has not said yet yeah okay then and then i want to re-improve the report because then i want to have information how much bunker is on board but even then you probably would just

[101:39 - 101:59] you probably would just re-approve the last one yeah i mean for me it doesn't really yeah okay as you say if there is an example which has 30 import reports maybe then you would really think of oh i don't want to kick all of them but we also have the function to

[101:58 - 102:18] function to select from and to so for me it doesn't really matter i'm okay with any of the options what i have to report approve them for correction of data i would do it and if it's it doesn't matter i'm also happy to just approve the

[102:17 - 102:37] And this is what I was wondering, Nguyen, do you see any issue with that? Yes. You do, right? Yeah. Because of the consumptions. Approved in between, we got the data wrong. Only bad approved because the system is designed that the previous is terrible.

[102:36 - 102:56] is taking back some value from the previous. Because of the consumption, right? Yeah. So always re-approving all, even all 50 import reports. It's more desire, it's more desire to get the data correct. Yeah, because otherwise we are insecure. As far as I see it, correct me if I'm wrong.

[102:55 - 103:15] But otherwise we would miss data on consumption and we would not implicitly feel the consumption from, let's say, birth to unbirth. But we would really need each and every import and consumption and then sum it up to have the correct figure.

[103:14 - 103:34] Yeah, but I mean we don't really have this situation so often, so I guess in those cases it's also fine to re-improve all. Okay, good.

[103:33 - 103:53] Then let's try to see if this one is still 19 This one is 148

[103:52 - 104:12] because the value is not being inputted so by default

[104:11 - 104:31] So by default, if the operator doesn't input anything, it will show the same value from the speed above. So now you see we didn't input any value in here. So actually the data is not having anything and the frontend is showing the same value.

[104:30 - 104:50] front end is showing the value from the above but if we try to insert anything it will get fixed by that moment but for all of the other things like this one and this one we didn't have it that's why if this one gets recalculated as an average

[104:49 - 105:09] as an average it will show down there but if the operator they try to change it for each of them so it actually should be pre-filled on voice creation so on voice creation whatever is the speed and the estimate should go here

[105:08 - 105:28] and then on voice creation of course this should be same because estimate calculated with dataloy same distance same speed and here they calculate with dataloy so they will all look the same and then once the reports roll in this black speed would change but this one would keep but then we need to look at voice creation

[105:27 - 105:47] at voice creation why they are not correctly mapped into here i think the voice creation it doesn't have that logic yet okay then i will look at that okay

[105:46 - 106:06] okay yeah I think that is it just want to show that we have the undo departure undo arrival and if we I don't know if we need the undo departure and arrival

[106:05 - 106:25] to be only available on the last or we can also make it to the middle like this one but changing the middle would have a big effect as you will see that we bring back the vessel from here to here and thus affecting a lot of reports that need to be re-approved

[106:24 - 106:44] need to be re-approved and then i'm knowing that is desired but it is there we can decide i would say it's nice if it if it really is there because sometimes i don't know why a mistake has happened two weeks ago and people want to make a change it will not happen very often

[106:43 - 107:03] not happen very often but if it's already there i think it should also stay yeah and i will keep keep it there and then see if we make use of it any in any situation yes yeah okay sounds good yeah

[107:02 - 107:03] Yeah, okay, I think that's it.



---
*Generated using Whisper large v3 and processed automatically*
