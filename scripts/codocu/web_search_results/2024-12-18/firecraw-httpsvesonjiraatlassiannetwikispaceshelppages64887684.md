

📖 **Crawling content from https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887684**...

Jump to

1. [Confluence navigation](#AkTopNav)
2. [Side navigation](#AkSideNavigation)
3. [Page](#AkMainContent)

Atlassian uses cookies to improve your browsing experience, perform analytics and research, and conduct advertising. Accept all cookies to indicate that you agree to our use of cookies on your device. [Atlassian cookies and tracking notice, (opens new window)](https://www.atlassian.com/legal/cookies)

PreferencesOnly necessaryAccept all

restrictions.empty

10 Jira links

Summarize

Welcome to the Veson Nautical Knowledge Base. In the [Help Center](https://help.veson.com), you can view the same articles and contact support as needed.

# IMOS - Bunker Planning and Estimated Consumption

- ![](/wiki/aa-avatar/557058:a64f1c7f-c328-46e3-9802-57a1a392c6f6)Former user (Deleted)

- ![](/wiki/aa-avatar/624210b0f6a26900695b64de)Melanie Whitelock

- ![](/wiki/aa-avatar/611d34609ee2e4006994371e)Minori Kato

- +4


Owned by [Former user (Deleted)](/wiki/people/557058:a64f1c7f-c328-46e3-9802-57a1a392c6f6?ref=confluence&src=profilecard)

Last updated: [Dec 12, 2024](/wiki/pages/diffpagesbyversion.action?pageId=64887684&selectedPageVersions=15&selectedPageVersions=16) by [Melanie Whitelock](/wiki/people/624210b0f6a26900695b64de?ref=confluence&src=profilecard)

7 min read

The Veson IMOS Platform is the market-leading cloud solution for commercial marine freight and fleet management.

In Bunker Planning, bunker prices are proposed based on purchase history, but you can change them, set up your initial quantities, and set up calculation methods for each fuel type. Fuel use is calculated by port, and you can enter quantities and prices for any bunkers you plan to receive.

To open the Bunker Planning form, do one of the following:

- On the Estimate [column](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887369#IMOS-Estimate,ColumnView-Toolbar "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887369#IMOS-Estimate,ColumnView-Toolbar") or [details](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887644#IMOS-Estimate,DetailsView-Toolbar "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887644#IMOS-Estimate,DetailsView-Toolbar") toolbar, click ![image-20241212-041744.png](blob:https://vesonjira.atlassian.net/d67b0d7a-1796-410a-9406-085fdfc4d1cd) or ![image-20241212-041803.png](blob:https://vesonjira.atlassian.net/2107c320-47a2-4547-b722-fedfac044d69) and then click **Bunker Planning**.

- On the [Estimate details](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887644#IMOS-Estimate,DetailsView-GeneralInformation "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64887644#IMOS-Estimate,DetailsView-GeneralInformation") fuel grid, either click ![image-20241212-041822.png](blob:https://vesonjira.atlassian.net/d04ce575-b209-4834-adf9-d08edbe8e840) or right-click a line item, and then click **Details**.

- On the [Estimate P&L panel](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886201 "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886201"), under Expenses, click the **Bunkers** line item.









Open image-20241212-041928.png



![image-20241212-041928.png](blob:https://vesonjira.atlassian.net/03ba8f54-d4d0-412c-919c-1ac842155ee2#media-blob-url=true&id=8a5d3318-3484-47f9-906e-3b6066fd4b64&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fpng&name=image-20241212-041928.png&size=31514&width=788&height=499&alt=image-20241212-041928.png)


Depending on the Vessel Type, the following columns will appear for heating, cooling, and reliquefaction, as well as IGS consumption.

- **Sea Consumption** is calculated based on the specified [consumption rate](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888086 "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888086") for the speed associated with the sea leg.

- **Port Consumption** is calculated based on the time used for loading or discharging, basis SHINC, at the Load or Discharge [consumption rate](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888086 "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888086") specified for the vessel. Additional time in port is calculated basis the vessel-specified Idle consumption rate. This additional time is Turn Time and time spent in port during weekend clauses. In addition, you can add extra time in port: The related columns are XP and Dem, which also count as Idle time.

- For **LNG** vessels, the LNG detail tab includes additional fields for \*\*OV Estimates only (not \*\*TO Estimates).














Open Ch-Estimates-Bunker Planning-LNG.jpg



![](blob:https://vesonjira.atlassian.net/e769e492-71fd-4e3d-9785-02ebc1780e17#media-blob-url=true&id=668ef947-c615-404f-b70f-2b2c7a39a9bf&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fjpeg&name=Ch-Estimates-Bunker%20Planning-LNG.jpg&size=89331&width=1041&height=502&alt=)









  - **Max Load**\- (Vessel Capacity m3 \* Filling Limit %) - Initial Bunkers m3

  - **Max Discharge** \- Loaded/Received Qty m3 - Total LNG Consumption m3

  - To back-calculate the optimal discharge quantity based on heel, right-click a discharge port and then click **Calculate Disch Qty based on Heel**.













    Open Ch-Calc Disch Qty from desired Heel.jpg



    ![](blob:https://vesonjira.atlassian.net/9ae06eff-25d0-4349-bd2e-d6e3334d21e2#media-blob-url=true&id=161f46aa-1a41-4e7c-ab15-7d4538d3cffe&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fjpeg&name=Ch-Calc%20Disch%20Qty%20from%20desired%20Heel.jpg&size=18459&width=369&height=161&alt=)











    Enter the **Heel desired upon arrival** and then click **Calculate**. To save the calculated Discharge Quantity, click **Save**.
- For **Bulk carriers**, there is an option for each port call to indicate whether the vessel will be using its own cranes. If not, it consumes at the Idle [consumption rate](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888086 "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888086").


Optimize Liftings for Cargo

For a type \*\*OV voyage, you can optimize liftings based on bunker prices at fueling ports specified in the Voyage Estimate Itinerary. You can also take into account the freight rate of one of the cargoes on the Voyage Estimate to determine if it is more beneficial to lift more bunkers in place of that cargo or vice versa.

On the Bunker Planning form, do the following:

1. Select the **Optimize Liftings for Cargo** check box.

   - To subtract the freight rate of one Cargo on the itinerary from the bunker price at the next port before the most advantageous fueling port is determined, in the field next to the check box, select a Cargo with Freight Type F.
2. Enter a bunker **Price** for each port at which you want to lift bunkers.

3. Enter an **End Quantity** greater than or equal to the safety Margin of the vessel.


The Initial Quantity is taken into account and the amount of fuel needed across all voyage legs calculates. When Prices are entered, Receive quantities automatically populate at the ports with the lowest price. Quantities are calculated such that the vessel arrives at the terminating port with a quantity equal to the specified End Quantity.

- If there are multiple fueling ports (indicated by prices entered) in the itinerary, the Receive quantities are automatically populated with the amount of bunkers needed to arrive at the first fueling port so that the ROBs are equal to the safety margin of the vessel. Then, at the second fueling port, the amount of bunkers are populated such that the quantity upon arrival at the terminating port is equal to the End Quantity specified.

- If you manually enter a lifting quantity, that amount appears blue and is not overridden when the calculation is run again.

- The optimizer calculates in real time; that is, Receive quantities automatically adjust when you change prices.

- The optimizer no longer calculates after the Voyage Estimate is fixed; it is for planning purposes only.


## Use Scrubbers

When the **Use Scrubbers** check box is selected, low sulfur bunkers are not used for at-sea consumption within [ECA zones](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886358 "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886358"). Instead, high sulfur ("H"-type in the Vessel) bunkers is consumed. In-port consumption still adheres to Vessel/Fuel Zone bunker configuration if a given port is within an ECA zone.

## Fuel Zones

For Estimates that are not already using Fuel Zones to calculate bunker consumption and have unsailed ports, a **Use Fuel Zones** button appears in the lower left corner. To recalculate estimated bunker consumption and cost based on information entered in [Fuel Zones](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888213 "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888213") in the Data Center, click **Use Fuel Zones**.

If you have configured a [Fuel Zone Set](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888213 "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64888213"), you can select it, rather than the Default set, at the bottom of this form.

## Why isn't my Estimate showing consuming correctly?

There are a few places you can check to find out why a vessel isn't consuming as planned.

- Open the bunker estimate and check the Fuel Zone Set


Open image2020-9-4\_15-1-18.png

![](blob:https://vesonjira.atlassian.net/7363d74a-ed70-49e2-ba33-fbb3f7ecfa5f#media-blob-url=true&id=5c471a12-f055-4799-b2ed-0f40860d2d31&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fpng&name=image2020-9-4_15-1-18.png&size=39473&width=938&height=623&alt=)

- Check the Vessel Details to confirm your fuel types are configured correctly. (Vessel Fuel Zone Set can be entered here)


Open image2020-9-4\_15-5-52.png

![](blob:https://vesonjira.atlassian.net/df43b665-5420-402e-b4eb-c2de26f608cd#media-blob-url=true&id=1c8a4437-f07d-48e8-b215-b8e0ff022892&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fpng&name=image2020-9-4_15-5-52.png&size=219355&width=1915&height=991&alt=)

- Within the voyage bunkers, make sure there is enough Primary fuel to complete the voyage. If there is not, the system with calculating with a backup fuel unless there is not enough fuel for the backup Fuel to complete the voyage or the disable backup fuel checkbox has been selected. In this case, the system will have the Primary fuel consume the entire voyage and the backup fuel quantity will be untouched. This is based on the assumption that a bunker lifting will happen, clearing the need to use the backup fuel for the voyage.


Open image2020-9-4\_15-22-52.png

![](blob:https://vesonjira.atlassian.net/a499e755-24fd-4012-9215-74aea2197b53#media-blob-url=true&id=fc4f1e8e-3f2d-4f82-a6e8-5318456f35e6&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fpng&name=image2020-9-4_15-22-52.png&size=222998&width=1915&height=991&alt=)

Open image2020-9-4\_15-23-20.png

![](blob:https://vesonjira.atlassian.net/ad978aa0-11fb-457b-972f-042e20d58522#media-blob-url=true&id=e73282e3-81f3-4411-b746-57845cd3dd7e&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fpng&name=image2020-9-4_15-23-20.png&size=225640&width=1915&height=991&alt=)

Open image2020-9-4\_15-23-37.png

![](blob:https://vesonjira.atlassian.net/3244a8b5-8b22-4f9f-927a-e4fd3bac5a23#media-blob-url=true&id=3f3d6932-ebcd-4429-be3b-ec5ea786da4d&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fpng&name=image2020-9-4_15-23-37.png&size=224849&width=1915&height=991&alt=)

Open image2020-9-4\_15-23-57.png

![](blob:https://vesonjira.atlassian.net/ee55f520-aaa1-419a-b36d-532ec7420c00#media-blob-url=true&id=96bb6b83-1e18-4e3a-aaa0-c85c497a096d&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fpng&name=image2020-9-4_15-23-57.png&size=226190&width=1915&height=991&alt=)

Open image2020-9-4\_15-24-12.png

![](blob:https://vesonjira.atlassian.net/4d0acc42-d63c-4491-b78a-d5fccf14c87a#media-blob-url=true&id=7b29173b-7353-4e9b-98ab-d6151ad06973&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fpng&name=image2020-9-4_15-24-12.png&size=226362&width=1915&height=991&alt=)

- Is this a copy of another estimate? If so the estimate will consume based on the fuel zones configuration during the time of the creation of the original estimate. We suggest making a new estimate or enabling the configuration flag CFGRecalcDistancesOnEstimateCopy.


Open image2020-9-4\_15-25-39.png

![](blob:https://vesonjira.atlassian.net/3086b24f-38d3-45ae-a6f8-04718bd12b47#media-blob-url=true&id=a3521049-6928-41f6-b5fd-9ba0eb9322bc&collection=contentId-64887684&contextId=64887684&mimeType=image%2Fpng&name=image2020-9-4_15-25-39.png&size=140437&width=1915&height=991&alt=)

- Have changes been made to the Fuel Zone configuration since the creation of the estimate? Estimates will calculate fuel consumption based on the configuration at that creation of the Estimate, new changes will not be shown.

- If an initial FIFO queue is populated for the estimate, editing the initial bunker price will now ask users if they want to replace the initial FIFO inventory with a flat price.


Related Configuration Flags

| **Name/Flag** | **Description** |
| --- | --- |

| **Name/Flag** | **Description** |
| --- | --- |
| **Enable Legacy IFO Top Off Calc**<br>CFGEnableLegacyIFOTopOffCalc | For LNG vessels, relates to the calculation of the amount of IFO (or other designated "FOE" fuel type) needed in order to accelerate to a given speed higher than the NBOG speed when in dual-fuel mode. When this config flag is enabled, this amount is calculated as the difference between (a) the IFO consumption at actual speed and (b) the FOE equivalent of the LNG consumption at the NBOG speed. When this config flag is disabled or by default, this amount is calculated as the difference between (a) the IFO consumption at actual speed and (b) the IFO consumption at NBOG speed. |
| **Enable Voyage Estimate Init Bunker Queue**<br>CFGEnableVoyestInitBunkerQueue | When enabled, Estimates allow multiple initial lots for each bunker type, similar to the Voyage Manager. On the Bunker Planning form, the **Initial** **Quantity** field label becomes a link that, when clicked, opens the Initial Bunkers form. These lots will be defaulted from open positions, TC In delivery, and in-progress voyages. When bunker consumption exceeds the available inventory for a certain fuel type, the end price for that fuel type is used to calculate bunker costs. If an initial FIFO queue is populated for the estimate, editing the initial bunker price will now ask users if they want to replace the initial FIFO inventory with a flat price if this configuration flag is enabled. |
| **Enable Scrubber Type**<br>CFGEnableScrubberType | When enabled, a scrubber drop-down menu appears on the Port, Voyage Bunkers, Bunker Planning, and Vessel forms accessed through an Estimate. On the Port and Vessel forms, the drop-down menu reflects scrubber values allowed at the port and equipped in the vessel. On the Voyage Estimate and Voyage, it reflects the scrubber type used for bunker calculations. On the Vessel form, the “Use Scrubbers” check box is replaced with the new “Scrubber Type” drop-down menu. The Fuel Zones form has two tabs to support “Scrubber” and “Non-Scrubber” configurations. These new options facilitate bunker calculations to use the [IMO 2020 regulations](https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886365 "https://vesonjira.atlassian.net/wiki/spaces/help/pages/64886365"). |

## Related pages

Collapse

[IMOS - LNG](/wiki/spaces/help/pages/64887620/IMOS+-+LNG)

IMOS - LNG

[IMOS Platform](/wiki/spaces/help/overview)

Read with this

[IMOS - Consumption Tab - Vessel](/wiki/spaces/help/pages/64888086/IMOS+-+Consumption+Tab+-+Vessel)

IMOS - Consumption Tab - Vessel

[IMOS Platform](/wiki/spaces/help/overview)

Read with this

[IMOS - About Vessel Consumption Setup](/wiki/spaces/help/pages/64886930/IMOS+-+About+Vessel+Consumption+Setup)

IMOS - About Vessel Consumption Setup

[IMOS Platform](/wiki/spaces/help/overview)

Read with this

[IMOS - Estimate, Details View](/wiki/spaces/help/pages/64887644/IMOS+-+Estimate+Details+View)

IMOS - Estimate, Details View

[IMOS Platform](/wiki/spaces/help/overview)

Read with this

[FAQ - Explanation of Bunkers on Consumption](/wiki/spaces/help/pages/403865742/FAQ+-+Explanation+of+Bunkers+on+Consumption)

FAQ - Explanation of Bunkers on Consumption

[IMOS Platform](/wiki/spaces/help/overview)

Read with this

[IMOS - Voyage Bunkers](/wiki/spaces/help/pages/64887872/IMOS+-+Voyage+Bunkers)

IMOS - Voyage Bunkers

[IMOS Platform](/wiki/spaces/help/overview)

Read with this

![thumbs up](https://pf-emoji-service--cdn.us-east-1.prod.public.atl-paas.net/standard/caa27a19-fc09-4452-b2b4-a301552fd69c/32x32/1f44d.png)

![clapping hands](https://pf-emoji-service--cdn.us-east-1.prod.public.atl-paas.net/standard/caa27a19-fc09-4452-b2b4-a301552fd69c/32x32/1f44f.png)

![party popper](https://pf-emoji-service--cdn.us-east-1.prod.public.atl-paas.net/standard/caa27a19-fc09-4452-b2b4-a301552fd69c/32x32/1f389.png)

Still need help? Visit the [Veson Nautical Help Center](https://help.veson.com).

Copyright © 2017-2024 [Veson Nautical LLC](https://veson.com/) All Rights Reserved - [Privacy Notice](https://veson.com/privacy) \| [End User Terms of Use](https://veson.com/terms/)

{"serverDuration": 19, "requestCorrelationId": "9df813b0625741a096f9bdbb3d97054b"}

📖 **Summarizing content**...

While the provided text focuses on explaining the IMOS system's features related to bunker planning rather than broader strategies, we can still extract some relevant insights:

- **Accurate Consumption Data is Crucial:** The emphasis on vessel consumption setup and detailed fuel zone configurations within IMOS highlights the importance of accurate data for effective bunker planning.  This implies that strategies should prioritize collecting and analyzing historical consumption data to understand a vessel's fuel usage patterns under various conditions (speed, weather, load, etc.).

- **Scenario Planning:** The ability to create "estimates" and view details like bunker requirements suggests that modeling different scenarios is a key aspect of bunker planning. Strategies likely involve:
    - Forecasting fuel needs based on projected routes, speeds, and potential delays.
    - Evaluating multiple bunkering options (ports, suppliers, pricing) to optimize costs and minimize operational disruptions.

- **Real-Time Monitoring and Adjustment:**  The IMOS system's focus on details like "voyage bunkers" suggests that ongoing monitoring of fuel consumption during a voyage is essential. This implies that bunker planning strategies should be adaptable:
    - Regularly comparing actual fuel usage against planned estimates to identify deviations.
    - Adjusting course, speed, or even bunkering plans as needed based on real-time conditions and data.

**Additional Context from General Industry Practices:**


While not directly stated in the provided text, here are some common bunker planning strategies used in the marine industry:

 - **Just-In-Time Bunkering:**  Minimizing fuel carried onboard to reduce weight and maximize cargo capacity. This requires precise planning and coordination with suppliers along the route.
 - **Opportunistic Bunkering:** Taking advantage of favorable prices or convenient locations even if it deviates slightly from the original plan.
 - **Hedging:** Using financial instruments to mitigate price volatility in the bunker fuel market.

Remember that effective bunker planning is a complex process that considers numerous factors, including cost optimization, operational efficiency, environmental regulations, and risk management. 
