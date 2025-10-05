# Video Transcription

## Summary
This document contains the transcription of the provided video file.

## Content

Transcription with Segment Timestamps:
[00:00 - 00:15] Hello Jan. So, in this video, I will try to encapsulate the knowledge about the few EU of which I have been learning. So, it serves as

[00:15 - 00:30] the validation to prepare for our next meeting to discuss on this topic and also to provide the qaqc team our code for you qaqc team

[00:30 - 00:45] a video for so that they can refer to to understand the feature when they have testing this one on VVMS okay so for Vue EU as I understand it is another

[00:45 - 01:00] kind of like penalty apply to the vessel when they try to emit CO2 into the atmosphere. So for CO2 we already have ETS which is emission

[01:00 - 01:15] calculated directly on the amount of CO2 that the vessel will emit during a voyage and the emission comes from

[01:15 - 01:30] burning the bunker to create energy so that it propels the vessel to move forward. So basically there are some parameters consider to calculate fuel yield. The very first

[01:30 - 01:45] value important value also is the lower calorific value and this one measures the total amount of energy generated if we burn one gram of the

[01:45 - 02:00] of the fuel. For example in here, if we have fossil fuel, if we burn 1 gram of it, it will emit this value of energy and there are another kind of parameters in here.

[02:00 - 02:15] the GHG represent for greenhouse gas so the well to tank greenhouse gas of CO2 represent for the expected CO2 emit into

[02:15 - 02:30] the atmosphere in order to extract this fossil fuel from the well into the tank so that the vessel can use. So basically what they say is that in order to generate one

[02:30 - 02:45] mega joule of energy for the vessel to use the extraction of this fossil fuel actually cost this value 14.4 gram of CO2 and in order to break

[02:45 - 03:00] To burn the fossil fuel, it will generate CO2, CH4, and N2O, which is also greenhouse gas, but all of them are calculated into the equation.

[03:15 - 03:30] well-to-weak greenhouse gas calculated for CO2 per megajoules which is 90.7 so basically what it communicates is that in order

[03:15 - 03:30] well-to-weak greenhouse gas calculated for CO2 per megajoules which is 90.7 so basically what it communicates is that in order

[03:30 - 03:45] to have 1 megajoules of energy for the vessel to use. The entire process from extracting the fuel until it is burned to create the energy will generate 90 grams

[03:45 - 04:00] of CO2 into the atmosphere okay so these two value is the one that our calculation heavily rely on the LCV is the amount of
[04:00 - 04:15] megajoule generated per gram of fuel and the well-to-weak greenhouse gas is the amount of CO2 equivalent per megajoule generated. And in order

[04:15 - 04:30] With these two values in mind, so if a vessel needs like 10,000 of tanks to go for the voyage, and 2,000 is burned inside Europe, and 8,000 is burned outside, so we can calculate

[04:30 - 04:45] the total amount of energy in scope is that we know the energy spent in Europe will have 100% factor and the value being burned outside Europe will have 50% factor just like

[04:45 - 05:00] this one so we have a thousand of tons plus with time with a factor of 15 percent and then each of these will have like this value of energy so it is just a

[05:00 - 05:15] and then a plus with these two so we got a total amount of energy in scope for fuel yield and thus we have this amount of energy in scope and also

[05:15 - 05:30] we have like a factor we have like a value for gram of CO2 equivalent per mega joule which is 90 and the policy says that by 2025 the vessel

[05:30 - 05:45] need to reach a target of only 89.3 grams of CO2 per megajoule so because we only burn this fossil fuel we are at 90 so for every megajoule

[05:45 - 06:00] mega joules used we will have an exist in the limit that the policies allow and thus we times with the total amount of energy we need we have like a total amount of

[06:00 - 06:15] shield to existing the limit that the policies allow so this is what they call a compliant balance and it can be positive or negative so basically the negative will

[06:15 - 06:30] stand for that we already exist the limit a positive mean that we are under the limit so this balance for the vessel can be combined into a pool of compliance

[06:30 - 06:45] for the vessel or for even multiple vessels so by the end of the year we will look at this pool if the pool at the end of the year is still a minus value that we need to pay a penalty for it because we exist

[06:45 - 07:00] the target of CO2 per megajoule but if we have a positive value then we can kind of reuse this one for the next year

[07:00 - 07:15] so it encouraged the vessel to start trying to lower the grams of CO2 per megajoules they generated to reach a better scenario that we

[07:15 - 07:30] reduce global warming because we reduce the total amount of CO2 emitted into the atmosphere. So with this example just shows that if we don't care about the policies we

[07:30 - 07:45] We just go ahead and use our fossil fuel as before. The moment we burn any fossil fuel, we will exist this value stated by the policy and thus we have the maximum value.

[07:45 - 08:00] value balance for every voyage and at the end of the year everything sum up into a big negative value and we need to pay a large amount of penalty money so that is basically

[08:00 - 08:15] what we already have in BVMS that right now we only calculate the penalty that is because we exist the amount of permitted CO2

[08:15 - 08:30] So, we have to calculate the penalty for each voyage and we sum up everything. But for BBC, it's not the case that we are interested in because what in BBC, as I understand,

[08:30 - 08:45] then we interested in more in in the scenario that okay so now I want to reach the balance equal to zero so I comply with the policies how much force

[08:45 - 09:00] I need to switch in order to like reduce the amount of fossil fuel and increase the amount of biofuel in order to have a better value of CO2 emitted into the atmosphere.

[09:00 - 09:15] megajoule generated so I will explain to you in more detail about that so same scenario in here we burn MGO exactly the same setup but because this one we have

[09:15 - 09:30] a wind-assisted propulsion attached to the vessel. So, in order to generate the same amount of energy, we now emitted at least CO2 into the atmosphere because the

[09:30 - 09:45] our CO2 per megajoule now it list because we have wind assisted so right now the amount is only 86 and the target is 89 so we are lower than the target

[09:45 - 10:00] of which at the end of the year will have a positive value. So you would imagine if this voyage exists after this voyage for the same vessel. So at the end of the year, we still have a positive compliance.

[10:00 - 10:15] because this one is just minus 300 this one is positive 700 so we still have like a positive balance okay so another example of fossil engineering

[10:15 - 10:30] that if we use fossil NGL instead of the MGL above here is the scenario this one can generate a lot of energy per gram of

[10:30 - 10:45] fuel and you see the CO2 emitted per megajoule is also very low compared to the other so if we use this one we will be lower than the target

[10:45 - 11:00] So at the end of the year, we will have a very big positive value so that we don't have to pay the penalty. However, the situation is this bunker can be very expensive.

[11:00 - 11:15] and it is not available so that we can easily bunker it everywhere. But if we happen to have it, it will have a lot of positive impact to this CO2 amount that we emit into

[11:15 - 11:30] the atmosphere okay so here come the biofuel that is our main target for fuel EU energy so fuel EU energy is

[11:30 - 11:45] that we need to try to lower our CO2 emitted per megajoule lower than this value and this value also reduce year by year so in order to do that we need to blend our fossil fuel

[11:45 - 12:00] with some biofuel because the biofuel as you can see it has is also even have much lower CO2 per mega joule even compared to the other one that you can see in

[12:00 - 12:15] here and the main reason is that in order to create this pure field it is created from agriculture from vegetable something like that so actually the problem

[12:15 - 12:30] of creating the CO2, the biofuel will have like a minus value on the CO2 because plants, they can absorb CO2 from the atmosphere. However, when we burn this biofuel,

[12:30 - 12:45] we also generate CO2 into the atmosphere but in the end of the day if we sum everything up we still have a pretty low value of CO2 per megajoule for this biofuel

[12:45 - 13:00] So let's say the same situation as above. But right now, in order to complete the voyage, we need 2,000 of this one, 3,000 of this one, and then another 2,000 of this one for the build.

[13:00 - 13:15] fuel so the calculation is how much energy generated by this fossil fuel we still have this value time a hundred percent because it's in you

[13:15 - 13:30] And for every gram, it generated this megajoule. So we time with this one. And for this value, we time with 50%. And then, generated with this amount of megajoule, we reach this total amount of megajoule.

[13:30 - 13:45] in scope and we do the same thing for the HVO we have 44 so the total amount of energy will be this one plus this one that we had that we reach this one

[13:45 - 14:00] Okay, so we need to pay close attention to this total amount of energy because it's the sum of these two fuels that we have on board.

[14:00 - 14:15] however there is a small tweaks to this one so the policy says that it can prioritize the allocation of biofuel other than the fossil fuel so we need to

[14:15 - 14:30] recalculate again this scenario that as if we burn this 2,000 megatons inside the EU even though we burn it outside but it can be allocated into here

[14:30 - 14:45] So the situation changes. Now we have 2,000 optons time with this amount of energy. And then we time with 100% because it is now in EU.

[14:45 - 15:00] reach this one as the new energy right and the total amount of energy stay the same we use this one subtract with this one so we have a new value of this one so basically the tweaks change

[15:00 - 15:15] the amount of fraction between these two energy instead of we have like 149 and 44 we now have 105 and 88 instead

[15:15 - 15:30] And this also affect the total amount of CO2 equivalent by the end. So you can see here. In order to calculate the equivalent of CO2, because now we have more than one

[15:30 - 15:45] bunker type right so we have to average this one out so it says that this one have 90 this one have 34 but we use this amount of this one and we use this amount of this one so every

[15:45 - 16:00] We have this value times this value plus this value times this value and divide by the total amount of energy. Now we only have like an average of only 65.

[16:00 - 16:15] of CO2 equivalent per megajoule because that is the allocation of how much we use for each of these bunker types, right? So, we would expect this value to be somewhere in between this value and

[16:15 - 16:30] and this value and finally we compare this value with the target of 89 every year so we are now have lower value compared to the target of that it will end up

[16:30 - 16:45] in a scenario that we have a positive amount of compliance balance at the end of the year so that explains the forward calculation of fuel eu

[16:45 - 17:00] In summary, it is just that firstly, we calculate the amount of energy we burn for fossil fuel as before, but if we also have the biofuel on board,

[17:00 - 17:15] And for the biofuel, we have like these parameters available. Then we can calculate the compliance balance at the end of the voyage. And thus, we provide this compliance balance

[17:15 - 17:30] to BBC so that they can manage this compliant balance for a group of vessel in order to minimize the penalty they have to pay at the end of the year.

[17:30 - 17:45] That is basically the concept. And in our next meeting, Jan, we will discuss on how we want to handle the scenario that, okay, so if we start with fossil fuel,

[17:45 - 18:00] Let's say if we start with this MGO, we will have like a minus balance like this one. And there will be a button that you can click in order to bring this compliant balance to

[18:00 - 18:15] zero and if we click that one the software will try to calculate the amount of fuel it needs to substitute from the MGL into the bio energy

[18:15 - 18:30] in order for us to reach the compliance to be 0. And after we successfully calculate the total amount of energy needs to be subtracted from MCO and it becomes 0.

[18:30 - 18:45] build MGO we can calculate the amount of metric tons we reduce on MGO and the amount of metric tons we need to buy for build MGO and thus the price

[18:45 - 19:00] different the changes in the price of the bunker because we need to reduce the cheap fuel and replace it with a very expensive bunker so

[19:00 - 19:15] there will be an increase in the bunker cost that we put as a P&L item into our final voyage calculation. So you would

[19:15 - 19:30] expect to see it like this one if there is if we just ignore we don't use any build mgo at the end of the voyage we will have like a penalty for few eu but if there is a click

[19:30 - 19:45] if we click that one you would expect the penalty to become zero so we comply and we don't pay the penalty however the price for the entire the price for the bunker expand for the entire void will increase

[19:45 - 20:00] because we have to switch part of our MGO into BO MGO but however as the policy say we also don't have to pay the ETS cost for

[20:00 - 20:15] burning the BOMGO. So we would also expect our entire emission expense to also be reduced because we switch to use BOMGO. So we just click

[20:15 - 20:30] up a button we can see the total TCE profit and loss situation changes so that is what we have in mind let's discuss about this one in our next meeting and thank you if you have any question

[20:30 - 20:37] you can ask me directly on Teams or Telegram okay thank you very much for your attention



---
*Generated using Whisper large v3 and processed automatically*
