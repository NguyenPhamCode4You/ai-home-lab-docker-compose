# Video Transcription

## Summary
This document contains the transcription of the provided video file.

## Content

Transcription with Segment Timestamps:
[00:00 - 00:15] Okay guys, can you hear me well? I think Gian will also join.

[00:15 - 00:30] I will do recording so this session will be in English in order for us to also have documentation so this topic today is about logging system

[00:30 - 00:45] how we implement the log and how would we use the logging to handle when the system go on the production

[00:45 - 01:00] Firstly, I want to say to us that we try to increase the amount of logs in our application from now on.

[01:00 - 01:15] There are two types of locks. As you already know, we have System Lock and there are Application Lock. The System Lock is something that you don't have to care about.

[01:15 - 01:30] lock will be already available when we run the application on our Azure environment the system will automatically lock the information there if there is

[01:30 - 01:45] API that failed or SQL Server query that got some problem we already have that kind of log automatically available in the Azure which we refer to as System log

[01:45 - 02:00] the other kind of lock that is available and is responsible of our depth is the application lock application lock you will need to write the lock yourself using the

[02:00 - 02:15] What we have already set up in our application, we use Serilog for now. And Serilog is kind of like very mature library on.NET that allows us to write very schematic

[02:15 - 02:30] on our favor so we can define the log can also be string to console which is the default one if you run our source locally it can also be string to file that we can write the log

[02:30 - 02:45] into some file and finally is the log that we can string to all the application including the application inside which is our currently setup and of course you could imagine we could have like a connector

[02:45 - 03:00] that string the log to something else like Grafana and all the platform as well but these three are the things that we are currently doing and on the level of production we will do it in the application inside

[03:00 - 03:15] And in here, when using the serial logs, you can also customly define the output template of the log And how would you use it? So in any of the code

[03:15 - 03:30] you can also dependency inject the iLocker here and also inject the name of the function that you want the locker to automatically support. So for example I want to take

[03:30 - 03:45] write some log for some heavy processing function like CalculateConsecutiveVoyage so I just inherit the logger here and put the ConsecutiveLogVoyage function name in here and thus I can provide the logging

[03:45 - 04:00] every time that I wanted to lock the information into our system provide it a message a customized message that later on we could easily find back the locking inside

[04:00 - 04:15] the application of which I will show you shortly together with where the function is originated in in this example it will originated from the function calculate and say consecutive voyage

[04:15 - 04:30] So it is basically what it is. We have the log available in our Azure, which is application inside over here. And the application inside

[04:30 - 04:45] Inside, we set up for different environments, but for now, I will try to involve the guy who is going to do the maintenance with us when we launch the application in the production.

[04:45 - 05:00] so basically the setup is to also have us developer to take schedule to take care and to also monitor the application for some days as the schedule go on so

[05:00 - 05:15] So this is our current application inside setup and in here you can also see that we have a lot of available predefined components that you can immediately look at to see the

[05:15 - 05:30] of our application, of which I will show you quickly for each of these one. Firstly is the application map. The application map is kind of like a quick overview will provide

[05:30 - 05:45] provide us a quick overview of all of the available components and its overall health in the system. So you know we have two different APIs, the void API here and the master API, and during

[05:45 - 06:00] the last like 24 hours the filter that we can also that we can also make this is the data from the last hours or we can select the last data for 12 hours and click on apply

[06:00 - 06:15] then the chart will render and display the overall health of the system so you see that the application our backend application here have like very um like less than one percent of the error

[06:15 - 06:30] originated from the void API and 4% of the error originated from the master API you can also see how many requests is performed on the availability health check that we also have to make sure

[06:30 - 06:45] that our application is working correctly and how much the call the request call to call to our database so during the last 12 hours you see that the

[06:45 - 07:00] API perform 700 call to the DB while the master data perform 800 call and then there is like a function task test these are our application Azure function and

[07:00 - 07:15] dedicated for the cron job and some other heavy processing that we are currently working on that has a 100% of fail rate because it could not connect the database for now which is also expected

[07:15 - 07:30] And also, I could see that there are some calls to our block storage would also end up in a fail, probably

[07:30 - 07:45] because we don't set up the credential for now but that is basically the quick thing that we can also just see for the last 24 hours how how much impact

[07:45 - 08:00] or how well the system is behaving based on a quick chart like this one and this is referred to system log everything is provided by default when we add the application SDK into both the

[08:00 - 08:15] front end and the back end so we already have this one so everything is provided by default the second good thing is that we can also

[08:15 - 08:30] monitor the high-impact API code by having the leave matrix here which is also very good that we wanted to kaiap line monitor in real time whatever is

[08:30 - 08:45] happening in the application so right now there are no no requests coming in but if there are like different requests that for example I can go to PVMS test and click on some estimate and

[08:45 - 09:00] provide some calculation and probably to try to save or update estimate which is refer to maybe code4u vessel to be sure

[09:00 - 09:15] So that we don't interfere with our customer data, click on save and go back to application inside.

[09:15 - 09:30] the leaf matrix started to show and during some incident that we already see we already and we already get some incident that the CPU got too high and then

[09:30 - 09:45] the system RAM just gradually grow up until the application die so with this kind of like real-time metric we can already see what is happening on the test system like how many

[09:45 - 10:00] and how much duration each of these requests is performing how much CPU that we still have as a headroom how much memory that we are currently consuming and what is the request that is failed in here

[10:00 - 10:15] you can also see it this is the leaf matrix and there are like my favorite part of the application inside is that we can quickly find the

[10:15 - 10:30] transaction or the lock back in the console itself without knowing too much about the code. So in here, the search section allows us to kind of like perform an elastic search

[10:30 - 10:45] all of the logs that we have right also all of the log that the system automatically read right into our application inside so in here you can see that there are some health check

[10:45 - 11:00] request, there are some post endpoints that is currently being called inside the call estimate null recall system. You can find all of them in here just by typing. For example, I can also

[11:00 - 11:15] file consecutive and then press on enter to see if there are any requests related to

[11:15 - 11:30] a consecutive calculation just recently happened in the last 24 hours which is not right now I can perform one to let the log flow into the system so

[11:30 - 11:45] in here also let's pick the code for you again and then just perform an update

[11:45 - 12:00] The feature of consecutive is that it update the current voyage and bring the information from this voyage to the next voyage. And it is quite a heavy calculation that you could immediately see in the leaf matrix the CPU will RAM up.

[12:00 - 12:15] for some time and of course we needed to wait a bit of time to see the actual log coming in yeah but we basically can find back the information

[12:15 - 12:30] later on in here yeah just let it run a bit and there are kind of like inspect here networking

[12:30 - 12:45] So if we click on any API that you can spot, there are like a correlation ID. X correlation ID over here. So this correlation ID is automatically

[12:45 - 13:00] by the application inside SDK in our frontend. What it does is basically it captures every single request that the frontend has, assigns a correlation ID, and then when this request reaches the backend,

[13:00 - 13:15] Whatever happens after that, it will also assign with this correlation ID. So with the single correlation ID here, if we try to find it back in our locking system, we would be able to see the completion.

[13:15 - 13:30] like circle of how the how the request is handled it inside of our inside of our system yeah there are kind of like that techniques

[13:30 - 13:45] That in here, the short thing is that you can perform quickly to find a lock of your interest by using the short text over here. So you can search for a specific amount of lock information.

[13:45 - 14:00] that you already know in your code when you do logger.log something then you can also find the text back in this sub-box here or you can also find the log that is related to a request

[14:00 - 14:15] by just copying the correlation ID and put it in here. In the future, when we needed to do kind of like support ticket on the frontend, what we basically needed to do is that if there is an

[14:15 - 14:30] on some important API, we could automatically provide a function over here on the frontend that sends support ticket and the support ticket just try to encapsulate the correlation ID of the request that failed.

[14:30 - 14:45] send it somewhere to our kind of like maintenance system and guy who is working on the maintenance system can find back whatever happened in with whatever happened wrong with that system

[14:45 - 15:00] single request in our application inside over here. Yeah. Okay. And then there are some other things that we can also make use of. There is a failure

[15:00 - 15:15] dedicated to only showing us the failure of our application. You can also perform filter by time. But you can quickly see how many requests that failed during the last 24 hours.

[15:15 - 15:30] hours how much we have and how many that fail and on the one that fail what is the one that fail the most you can already saw the impactful API over here that we

[15:30 - 15:45] we might need to check on this one and then we perform some optimization to reduce the amount of failed API call in here. And of course, the final thing,

[15:45 - 16:00] And this is for the guy who is very interested in the in the logging is that you can perform custom query to get the to get the log information that you design.

[16:00 - 16:15] The query is kind of like a simple query that they define as KQL. You can also use the AI to generate the KQL for you, which is they are very famous. So AI can handle it pretty fast.

[16:15 - 16:30] But whatever you have in mind, you can also write a custom KQL for it. For example, I want it to find every single request that happened in the last 15 minutes not contained as healthy.

[16:30 - 16:45] because I don't want it to see the service health tracking request perform to our application but I only wanted to limit down the request that is calling from to our BVMS website

[16:45 - 17:00] and BVMS master backend and then I get this information out select top 100 whatever it is and then I got the information I want to see over here

[17:00 - 17:15] and then using this information to find the maybe some API maybe on some specific time range over here that you know there are some API impactful API that cause the system to respond

[17:15 - 17:30] very slowly then you can perform this query to find all the requests that fall in that kind of lifetime range and then you can yeah try to figure out what is wrong by the data display here

[17:30 - 17:45] Of course, there are some workbooks that are already developed by Microsoft. You can also try some of these workbooks here that we can also perform and write some

[17:45 - 18:00] custom dashboard for ourselves. Microsoft already provides us the components, the tools to make this happen. We can drag and drop the component and then assign the component with the data to let it work.

[18:00 - 18:15] render to see some information custom by ourselves so for example in here you are seeing the request by location which is a custom workbook developed by Huy and we are showing how many requests

[18:15 - 18:30] is performed by different locations of the application. You can also write your own custom workbook or try to get familiar with the existing workbook that Microsoft already provides for us.

[18:30 - 18:45] and then there are like an alert thing that is all of the information related to the log then there are like an alert system that we can also

[18:45 - 19:00] In here, you can create custom alerts based on your need. You can choose by default what is the metric that you want to get an alert from.

[19:00 - 19:15] For example, you can make an alert if there are so many failed requests over here. And then you can also try to find the threshold that you think would make sense to have an alert

[19:15 - 19:30] If the information exceeds this threshold, then you can make a fire alert to somebody else or to some guy who is doing the maintenance By changing the amount over here, for example

[19:30 - 19:45] If the threshold is bigger than 20, then I wanted to see the, I wanted to have an alert if there are so many failure requests, there are like more than 20, 20 failure requests.

[19:45 - 20:00] for a single time frame over here and microsoft also display in here if we set it up if we set it up this alert like this one then what would be the moment that it got fired

[20:00 - 20:15] from the past data that we got here so if we choose this one too small you see it will be triggered three times but if we choose it bigger it will only trigger only one time but i think it is

[20:15 - 20:30] so you can also create your custom alert over here and then on the action tab you can also select what is the action to do

[20:30 - 20:45] when this alert fired. You can also predefine some action of which I already tried is that I wanted to fire an alert via an email for the system health for some

[20:45 - 21:00] for one email and also for one Azure app So there is an Azure application that you can also install on iOS and Android and then log in with your Azure app

[21:00 - 21:15] with your account over here or over there and if your account is assigned as like a reader a log monitoring reader inside our application inside and then add it into this group then all of the alerts

[21:15 - 21:30] will start it to make it way to your email inbox or your notification app so that is basically what it is how the how the alerts look like I don't quite

[21:30 - 21:45] like it for for now because the information kind of like all over the place but at least the locking is there so it sends the event at what time

[21:45 - 22:00] what is the name of the alert and on what application inside that send to your email or your mobile phone notification

[22:00 - 22:15] yeah i think i needed to accept somebody in but let's see okay

[22:15 - 22:30] So basically that is our alert but I'm not quite happy with what we see in the default alert system

[22:30 - 22:45] It is nice that we can set up very flexible conditions over here. There are places that we can also write a custom code to trigger the matrix.

[22:45 - 23:00] basically do the metric definition on ourselves and then we define the action of which we do what with the when this thing happened right so for now we can send notification we can

[23:00 - 23:15] send email but of course we can also do something more technically I would say okay is there anything else on the application side

[23:15 - 23:30] And of course there are a lot of other stuff that you can try. But to me, what we needed to be very aware on the locking system is that

[23:30 - 23:45] On the dev side, we will need now to start producing more logs into the system, particularly the function that is business heavy that we wanted to see the log back.

[23:45 - 24:00] So, we need to write the application log there. And on the application inside dashboard, developers will take turn to do the scheduling maintainer, to become scheduling maintainer.

[24:00 - 24:15] we needed to get ourselves familiar with this one. Firstly, to see the overall health of our application. Second is to see the leave matrix if there are kind of like incoming impactful requests that we want

[24:15 - 24:30] to perform or we want it to observe. Click on the leave matrix and try to figure it out what could go wrong with the request that we know for sure is having performance problems, for example the shirt over here

[24:30 - 24:45] is the is the thing that we we can quickly find any log related to our application by having kind of like an elastic shirt

[24:45 - 25:00] we can search for the log text that we we have we can search for the correlation ID as I just show you how we can get the correlation ID from the request for some reason

[25:00 - 25:15] it is not showing for now but yeah I will figure it out why it is not showing but in here is a quick way that you can find out the pass information 24 hours the lock that is

[25:15 - 25:30] on your on your spot. Just put the text here and it will show. And then availability is in reverse to the the failure thing is that you can see the overall

[25:30 - 25:45] the current overall health of all of our backend API over here. Webapp, master data, voice, all of them is currently working. Failure rate is the summary of what failed the most.

[25:45 - 26:00] and give us information on which API is currently failing too much that we wanted to take a look on. And also, finally, the log here is the place that we run

[26:00 - 26:15] Write custom log. This is the thing that you would probably use the most when you become the maintainer of our system. If there is some case happen and we wanted to figure out more information, you can write the custom log.

[26:15 - 26:30] custom kql over here execute it to get the information you want and of course you can write all of the kql and then assign them to kind of like a workbook and then we have some

[26:30 - 26:45] custom dashboard on our own, of which we can also write our own customized dashboard that I can also show you quickly, maybe.

[26:45 - 27:00] So, might not be this link, also not this link.

[27:00 - 27:15] So, based on this one, you can also write, of course, you can write the kql in here and then use the component defined by mysql.

[27:15 - 27:30] to render out the visualization just like what we just did one KQL aside to a map component and it render and we can also do same with like

[27:30 - 27:45] of like a custom application that we can develop but for any other application what we need is a client id and a client secret and an app id that we need to register into the application inside

[27:45 - 28:00] and then using this information we can connect to our application inside workspace to get the log to get the login and in here we have

[28:00 - 28:15] some of the custom KQL that I asked the AI to do. So all of the things that you are seeing is not a single line of code written by any developer. Just the AI prompting will be sufficient.

[28:15 - 28:30] for this one for this kind of work let me wait it is application inside inside

[28:30 - 28:45] So, for example, there are some custom KQL that I wanted to see total requests, how many valid requests, what is the average response time for all of the requests happened.

[28:45 - 29:00] during the last duration, which is a parameter that we can also input What is the error array, availability, memory usage, slowest API, percentage, whatever it is So if you have kind of like a metric you wanted to monitor

[29:00 - 29:15] on yourself you wanted to have like a custom KQL write it test it with the application inside log to see how it run and then write ask the agent

[29:15 - 29:30] to just like create some simple simple component to display whatever you see here so in here you see how many requests that we have for the last

[29:30 - 29:45] for the last one hour that go into our system what is the average response time in average for all of these requests how many of them is returned 200 status

[29:45 - 30:00] cost or the success how much dedicated memory as average and how much CPU is consumed and in here I for example myself I wanted to see the color

[30:00 - 30:15] between the amount of the request and also the the average response time of the request by the time frame in the last maybe one hour so from A to B

[30:15 - 30:30] These are the amount of requests in blue, which is very small, but the amount of time, the average response time of all the requests in one section, maybe for two minutes is kind of like one minute.

[30:30 - 30:45] this is like 1 second 1000 ms is 1 second so the response rate is not it's not too performant I would say so with this component if it end up with

[30:45 - 31:00] a very long red candle I already saw that our system might respond slowly because the every response time of all of the requests is existing 1000 millisecond with this one one second

[31:00 - 31:15] which means that our system is responding slow and just like the workbook that you see we can also have a work map on how many requests by region we have and in here

[31:15 - 31:30] we can define some top top 8 or top 10 results on all on the most call it api that we have so immediately we can spot the api that got call it

[31:30 - 31:45] so many times during the last one hour and what is the top slowest API in here display also the error distribution so all of the hundred percent

[31:45 - 32:00] of all of the errors happened in the last one hour have the fail rate of 405 which gives you some idea on what could go wrong and finally is how much

[32:00 - 32:15] request fall into each percentage defined by Microsoft and some more details like the top exception that we have for example we got like 12 instance of invoice not found

[32:15 - 32:30] error but this is kind of like a system error which is not handled by our code that is why it looks this way if the error is coming from the application

[32:30 - 32:45] I would say it would have more meaningful error but this is what we have as a default if the developer don't write any logging and the system perform wrong

[32:45 - 33:00] these are the things that we see and also display the requests in the last 15 minutes for example 100 requests from the last 15 minutes

[33:00 - 33:15] And then refresh rate is 2 minutes. Every 2 minutes it will perform a complete refresh to display the data again. So what we just go over is how...

[33:15 - 33:30] the entire flow of the log and for now will be the discussion if you have any question you can feel free to ask and what we just covered is how the log will propagate from

[33:30 - 33:45] our app into the application inside and how we developer as a maintainer later on can get the log out again to figure out what could go wrong with some specific request or to perform like

[33:45 - 34:00] real-time maintenance when our application goes online. I think this is the first session. Is there any question? I would be happy to answer.

[34:00 - 34:15] Is there anything else that we could miss?

[34:15 - 34:30] This section will not cover the mitigation yet For mitigation, what would we do if the system behave wrong?

[34:30 - 34:45] what would we do if the for example if there is like an impactful features that got it into the production then we wanted to revert it back those are the thing that happened after we

[34:45 - 35:00] successfully get the log and identify the problem. But what would happen next? We needed to have like a schema on the things that we needed to do. Of course, it is not on the shoulder of the guy who do the real-time monitoring.

[35:00 - 35:15] The guy do real-time monitoring just needed to know what go wrong, can identify which API is causing the wrong, but the fix would be delivered to the team in charge. And what would we do after that?

[35:15 - 35:30] For example, we rollback, we revert database, or we deploy quick fix will depend on different situation. But that is another topic for discussion.

[35:30 - 35:45] Yeah, right. Nguyen. Yeah, go ahead. Okay, hello. Okay.

[35:45 - 36:00] Okay, I know why we need the correlation ID into our system. Okay, so every single request.

[36:00 - 36:15] For example, if I click perform calculate over here, and then on the network section, every single API request will have correlation ID automatically.

[36:15 - 36:30] added by the application inside at this gate on the front end. Yeah. And this application correlation ID is attached to the backend that handle this request and also on all of the SQL query

[36:30 - 36:45] that go into that. So with this correlation ID we can see the entire life circle of the request when it was sent from the frontend and when it was handled on the backend.

[36:45 - 37:00] of which I could not show for you right now but just a simple capture of this correlation ID and then put it in the transaction search you would be able to file it or you can also write a custom

[37:00 - 37:15] log query to get all of the requests that have this correlation id equal to this one then you will be able to find all the information in the application inside yeah

[37:15 - 37:30] Yes. Yes, I understand. I just want to add another idea about the cooperation. For now,

[37:30 - 37:45] But I know we only have the one machine for our application. It's the backend, right? One server, one machine, right? But that has been changed. So now every environment has a dedicated machine.

[37:45 - 38:00] Okay. So for the app my experience for trace entry request, the lifecycle of the request, the

[38:00 - 38:15] end-to-end because we only have one merging, we can filter by the merging ID, something like that. But the collection ID is a good idea.

[38:15 - 38:30] And I would like you to add if you phone, if we have the micro service, you know, when we have the micro service, we have to mine many machine ID. We cannot like.

[38:30 - 38:45] filter the entry log end-to-end of the request. So the correlation will be useful in that case. Mm-hmm. Yeah. The correlation ID, I would say,

[38:45 - 39:00] This is already the smallest piece of information we have in the log life circle and it automatically creates per request We don't have to do anything, the library already do it

[39:00 - 39:15] But of course, because right now every environment have a different place, so we needed to know which application that the log will send into.

[39:15 - 39:30] So, for example, all of the information related to the test environment will be sent to this test application inside, but maybe the dev will send it in here and then the production will send it in here.

[39:30 - 39:45] So we needed to know exactly where the log will end up and then we can find the correlation ID in the subsection over in that specific application inside. We could not find it in a different application inside.

[39:45 - 40:00] Okay, that's good. Yeah, I understand. Hi, sorry I didn't follow my email.

[40:00 - 40:15] I saw that there is a separate site that we can use for monitoring the logs, right? Can you show me again the site?

[40:15 - 40:30] that we can monitor the service box. Monitor the service box? What do you mean by that?

[40:30 - 40:45] you wanted to see all of the requests related to Voyage API, something like that? No, I don't want to see the Voyage. I want to see the service log, meaning the log produced by the service. Whenever we have the log

[40:45 - 41:00] command in the code, we will produce the log somewhere. And definitely there is one place which is the Azure application inside. We can monitor that log

[41:00 - 41:15] Yes, so my question is do we have another or separate design that we can use for monitoring the backlog?

[41:15 - 41:30] and the part of the presentation that you show or separate the side, which if we can use for building the ROC one. Yeah, correct. Yeah. Okay.

[41:30 - 41:45] Can you share the screen and do the tracking log in that time?

[41:45 - 42:00] um uh maybe i didn't share with you i didn't share the screen here

[42:00 - 42:15] Just a quick overview is ok. So in here.

[42:15 - 42:30] When you were able to go into the application inside, then you can quickly go into the application inside that you know the lock will end up in.

[42:30 - 42:45] There are two ways that you can find a lot via a quick transaction search tool over here. You can make use of this single search box to perform, for example, you can perform like

[42:45 - 43:00] can I see the can I see the the lock the actual lock that yes of course that that I mean every lock that

[43:00 - 43:15] due by the service in the past like five minutes yeah of course so you can change the uh last hour or last 30 minutes is the smallest amount

[43:15 - 43:30] you just don't put anything just refresh and then you will find every lock that go into

[43:30 - 43:45] Like, can you click to the detail of one? It seems to me that it is the AGI tracing. Yes, correct. If it didn't, no, this is not good.

[43:45 - 44:00] Not what I mean, I mean the lock key transferred to the lock command, which is forwarded by serilock and will probably populate somewhere in the site.

[44:00 - 44:15] that we need to see. Any idea on the log information that you would see? For example,

[44:15 - 44:30] For example, in the let's say estimate update, estimate time.

[44:30 - 44:45] Okay, so here's the thing we have to trace by the request, right?

[44:45 - 45:00] all of the log related to some estimating including if the estimate exists in the request url or if you write logger.log and then estimate something it can also give

[45:00 - 45:15] it in here I mean this this lock is specific this is actually the correlation lock is actually

[45:15 - 45:30] API code, right? It starts from the request, estimate something. Is that the case? It will work for both. It will work for both because in our application, we don't have

[45:30 - 45:45] I can also find some lock. Yeah, let's say, let's say, yeah, let's say we, we go to update hasBeenMadeById, and that is the,

[45:45 - 46:00] the big flow right yeah but update estimate do we already have the log in that or update for us or anything

[46:00 - 46:15] Or update shipment, I think. Could be. I would say, yeah. Update shipment by ID. Yeah. Yeah. So, for example, here, I probably, I will have a... No. No.

[46:15 - 46:30] But could be the synchronization service request have some lock in here? Yes. So, can you find... Yeah, right here.

[46:30 - 46:45] I would like to see this layer block. You can just put it over here, the entire text.

[46:45 - 47:00] so you see there is a matching lock direction and you can also click on that ah ok ok so there is a single line in the one lock is the screen lock

[47:00 - 47:15] printed out there's a single line in it yeah okay okay so the next question the next question is can you can do we have enough

[47:15 - 47:30] another site, another website which can use this application inside or this is the only place. As I just showed.

[47:30 - 47:45] There are two ways, right? The guy who do maintenance can be added directly as a log monitor to the application inside. And then we got every tool available in here. But the other way is that we develop something like this.

[47:45 - 48:00] this on our own, and then write the customized version of the thing that we do, and provide this link to the dev guy. Yeah.

[48:00 - 48:15] The raw search here, can I do the raw search which contains all the logs in this time? Is it like 10.13 times? No, this is just something that I created.

[48:15 - 48:30] for myself to see the matrix that I find interesting the most. And I don't have a kind of like a short box and then transform it into KQL just yet. But something like that can be developed.

[48:30 - 48:45] I would say easily by the AI Okay, so we can think from for me for me each listing every lock command is enough because I I don't think I

[48:45 - 49:00] everyone have a credential to application inside, and should not be the case. And we, it should be good if we have another site for tracking the log, because tracking the log is the development

[49:00 - 49:15] and crucial need, but for application insight is not that much. Application insight for monitoring for production support, but more

[49:15 - 49:30] but tracking log is development control. So it would be good if we can separate a bit. If not, we have to limit the, let's say, permission. Yeah.

[49:30 - 49:45] I think anyway we would need to manage permissions even if we have a custom developer here. So we would need only our dev to be able to access or at least to have the account to

[49:45 - 50:00] view the log in this link so it is still the same the same thing that we need to set up permission whether we set up permission in the application inside itself or we develop things on our own and then set it up

[50:00 - 50:15] What we could also do is that right here we can have like a public or a company repository that the guy can just download and download.

[50:15 - 50:30] And then for everyone who is interested, they can have their own version of the log dashboard developed by themselves or by the AI. Then the guy, when it is their turn to monitor the application.

[50:30 - 50:45] They just run the app locally using the credentials that we have. So this side is running by your local server, so it actually doesn't connect to the internet, right?

[50:45 - 51:00] uh yeah it connected to the internet in order to connect to the azure application inside to pull the lock in yeah but does it go but does it go outside

[51:00 - 51:15] Yeah, it does not It does not expose this one to the outside, but if you have the wide guard you can access it Okay, okay, so it's exposed to local internet network. Yeah, it's exposed to outside

[51:15 - 51:30] The guy who has the white guard, who is our company VPN, will be able to access all of the resources related to this link.

[51:30 - 51:45] is not available for the public network? I think for now the most important thing for every developer is you guys have access to build only

[51:45 - 52:00] Let's say whatever platform and you can view the log for own dev environment, which is our internal finance, but not maybe staging.

[52:00 - 52:15] And you guys can perform some action and see the log going there. So that, for me, that is the most important thing at this moment. The rest, meaning the monitoring, the application insights,

[52:15 - 52:30] is for the one ending their production support and later on maybe monitor production, not necessary for all the guys.

[52:30 - 52:45] the log, checking the log in every development environment is necessary. So probably we may spend some time for setting up this and you can

[52:45 - 53:00] Please pay attention to this requirement because this is necessary for all of us. I think if it is a quick thing, we can set up the alarm.

[53:00 - 53:15] one local account that you can use to access the log and immediately see the log if that is required for your workflow. That is the quickest way that we don't have to do anything besides that.

[53:15 - 53:30] But on the long run, what we basically do is that we develop something on our own to provide the tools so that the developer can also make changes to it to get whatever the log we have.

[53:30 - 53:45] and transform the data, display in the chart, whatever it is. But we manage via the application ID. So it is more secure this way. Okay. Okay. So I will... Maybe I will...

[53:45 - 54:00] Yeah, I think it's a very interesting center, and that's all from me.

[54:00 - 54:15] I have a question. When we have a bug, an exception, how do we know the user who created the bug, or how do we proceed with the steps they create the bug?

[54:15 - 54:30] That I would say is not something that I can answer, but something like that we needed to have like a custom module in the frontend that we automatically capture.

[54:30 - 54:45] kind of information the application ID SDK it provides us the correlation ID I don't know if if the SDK also provide all the matrix available something like that we needed to check but we can

[54:45 - 55:00] obviously write some custom front-end logic that if there is a request fail we automatically capture the correlation ID capture the user ID that is having the trouble and even though the user doesn't

[55:00 - 55:15] submit a technical support ticket we just get that information and push it to somewhere in in our system then we can later get it back

[55:15 - 55:30] Do we have any app for the funnel to capture the user activity on the funnel side?

[55:30 - 55:45] For sure it will not help because it easily fall into privacy problem if something like that happen. Because we capture the screen activity of a user with this.

[55:45 - 56:00] maybe not like we will not capture activity like the video we can capture activity when user input something or they have action like set or calculate we can action the step

[56:00 - 56:15] I think that could be a nice idea that if we can also attach the user

[56:15 - 56:30] ID into the log and then on the log side in the KQL we just write custom KQL find every single log related to this user ID for the path like

[56:30 - 56:45] five minutes and then we see all of the api all of the action that the user perform in in a time order then we can spot what is he's doing on something like that

[56:45 - 57:00] yeah but this is uh k by k specific but something like that we can build okay

[57:00 - 57:15] And if there's no more questions, I think that is conclude for the first part. If you have some more questions, you can send it to me or to the group.

[57:15 - 57:30] video recording will also be available at some time later I will let you know okay then guys thank you for attending I will let you know when the content is

[57:30 - 57:41] ready to revise and if you have question you can just let me know



---
*Generated using Whisper large v3 and processed automatically*
