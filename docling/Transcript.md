Transcript
October 9, 2025, 8:33AM

Khoi Nguyen Pham started transcription

Martin Kuechler 0:03
Uh, I will share it in a second.

Khoi Nguyen Pham 0:04
OK.

Martin Kuechler 0:06
Let me just start that. I think it's a bit easier to to to draw a little bit. All right, I will share my screen.

Khoi Nguyen Pham 0:13
Mm-hmm.

Martin Kuechler 0:17
Um.
This.
Yeah, can you see my screen?

Khoi Nguyen Pham 0:26
Yes, I can see it.

Martin Kuechler 0:28
All right.
So, um, so the basic idea of, uh, CQRS just that we.
Talk about the same thing is is like separating queries from commands, right? So and.
So it would be, oh, my keyboards. Wrong language again. OK, so query. Yep.
Um.
Or often it's more like this way. So and and now there are a lot of details that that that could be different.

Khoi Nguyen Pham 1:10
It only.

Martin Kuechler 1:21
And it would still qualify it as CQRS, so to say. So often you will see that you have like of a two types of databases that you have a a main database. So this is kind of the.
The truth to say quote UN quote right and and this is like a a read database.
Read DB and there could be multiple of those and you you you can have different forms of those and yeah, so I I think this this is something you already know, right?
So it would would would go like like this and then it writes to these one and if you no other way around yeah and if you if you query this then so so this is one of the I would say purer forms of of secure I S.

Khoi Nguyen Pham 2:12
Yeah, perfect. Yeah.

Martin Kuechler 2:23
But in my experience I had with some some projects, so we we headed for DNV for for their shipping.

Khoi Nguyen Pham 2:32
OK, Mr.
Mm.

Martin Kuechler 2:38
Software they they also planned something like this and yeah in the end it was kind of overkill and and I think to to to to estimate whether it's overkill or not we we.

Khoi Nguyen Pham 2:48
Uh huh.

Martin Kuechler 2:55
We should look at the idea behind it and the the idea often is that you have.
Um, I mean something like Amazon for example, right? Uh, they they have a product.

Khoi Nguyen Pham 3:09
Mhm.

Martin Kuechler 3:13
Product and you have a lot of users that try to buy it at the same time, right? So you you have kind of a a a conflict because all of those users are are working on the same data because that you have.
You have in stock maybe only five items, but you have hundreds of people who who want to buy them, like like for tickets, for example, like ticket, ticket shops for for concerts and stuff like that.
And and with that you have like this shared data problem, shared state problem because on the page it says I have 5 and now everyone thinks yeah I can buy it. So if if the first one.
Access this with an kind of old school where where you where you mix the the the the command and the query. Then of course you you can have the problem that this gets locked in the database.

Khoi Nguyen Pham 4:04
Mm.

Martin Kuechler 4:17
And all the others are timing out, for example, or they see something. Yeah, so this is the main problem. So now if you if you spread that apart like like in this in this way, then of course those.

Khoi Nguyen Pham 4:25
Hm.

Martin Kuechler 4:35
Commands would be sent and it's not locking the data because we're like in in the most pure way we are recording like events.
Like ordered and then the next one comes ordered and and so on, right? But this.

Khoi Nguyen Pham 4:56
Hmm.

Martin Kuechler 5:03
Yeah. And then you have the syncing process to here and then a new number shows up and so on. So. So it could could be the case that they order and order and order and then afterwards they received their e-mail. Yes, your order went through or no, you you were too late or something like that, right. So.

Khoi Nguyen Pham 5:22
Hmm.

Martin Kuechler 5:23
But it does not block kind of the the the entry in the database and with that doesn't block the the interaction in the front end. But of course now you have a different problem and the the the problem in in my experience is.
The biggest or the most important thing about this is is not a technical one, it's more of a business modelling problem. Because if you model it like like this, like Amazon does it, for example, when you order you you don't.
See the answer, yes, you got it that they always tell you we received your your order and we will tell you what is happening next. So this is an asynchronous process that that they that they're doing because they're doing a kind of CQRS way.

Khoi Nguyen Pham 6:10
Yeah.

Martin Kuechler 6:21
To handle the ordering process because they wanna exactly they they don't want the case that's that's that this gets blocked because there's so many people that that are working on the on the same item.

Khoi Nguyen Pham 6:38
Hmm, yeah.

Martin Kuechler 6:39
So that's the the the the the idea behind that. And so that means if you if you think about secure OS, you should have a domain problem that's that's.
That's matching that that it's matching this, this, this architecture. I mean, and if you take another step back and think about separating commands from queries, that's a good idea no matter what. But the question really is, do we need?

Khoi Nguyen Pham 7:04
Hmm.
Hmm.

Martin Kuechler 7:14
More than one database? Do we need this syncing process and so on? Or could this the simple way would be to have just one database the the way you have it right now, right?

Khoi Nguyen Pham 7:25
Yeah, correct.

Martin Kuechler 7:26
So you have one DB and you're already separating.
I mean in a from a concept point of view you you have your mediator pattern with your commands and queries, right? So you in that way you're already separating that and.

1.  If you you would like to go that next step with all the stuff down here, that's that's the the nitty gritty part and that's the the thing that then would change the way you would handle your.
    Your business cases, so like you you you would have to model differently and I'm not sure about that. So we talked about the number of customers you have and as as far but but maybe you can help me as far as I understand.

Khoi Nguyen Pham 8:13
Hmm.
Yeah.

Martin Kuechler 8:28
The the business model, so so the the business workflows in your software, you rarely have the case that you have a lot of people that that write to the same data.
Is that correct?

Khoi Nguyen Pham 8:45
Yeah, the right would be correct that there's not many cases that a lot of people will write to the same record in the baby, yeah.

Martin Kuechler 8:54
So yeah, so and with that I think the this the part of CQRS down here is overkill for you.

Khoi Nguyen Pham 9:05
Mhm Yeah.

Martin Kuechler 9:06
So so that that you have separated out from a from a concept point of view logically that that you have commands and queries. That's a good thing that you're already doing that and I would suggest you you keep doing it. It's it's a good thing.

Khoi Nguyen Pham 9:23
Hmm.

Martin Kuechler 9:23
But with the amount of users and the amount of data and with the with the the the the business cases you have, I think it's it's it's totally fine to have one database and to keep it simple.

Khoi Nguyen Pham 9:37
Yeah.
That that I also agree the the benefit of having secure S in here. I would say for us is only that we are more traffic resilient on the query side. So basically we can have a lot of read replica of the same.

Martin Kuechler 9:59
Mhm.
Yeah.
Yeah.

Khoi Nguyen Pham 10:18
So the query the guy who needed to look for the data, they can directly query from the slave DB and that slave DB located in their own region. So the speed can be faster. I think about that but.

Martin Kuechler 10:26
Mhm.

Khoi Nguyen Pham 10:34
To be honest, applying the entire solution just to increase the the get query performance is not is not like a priority right now. We we also think about that but.
Yeah, the the way we set up our production environment already is that we have a main DB and that main DB is located in Germany West region of of Amazon.

Martin Kuechler 11:03
Mhm.

Khoi Nguyen Pham 11:07
And then there is another like a failover DB located in Southeast Asia and there is a mechanism that automatically synchronize the data from the main region to.
The Southeast Asia region I have test the ability that the data got sync and also the scheme matching also get sync very nice and it happened less than 10 minute. Yeah so the mechanism is already there but I don't force.

Martin Kuechler 11:33
Yeah.

Khoi Nguyen Pham 11:38
The the architect to also use the the order DB as a query teams.

Martin Kuechler 11:46
Right and and and this is one thing I think where you where you can really use that is or where it's a good idea is to have like regional.
Yeah, regional read copies, region A and and so on, right? And B&C. But this is then on the level of the database and is the like Azure can handle this, AWS can handle this and so it is not.

Khoi Nguyen Pham 12:06
Yeah.
Yeah.

Martin Kuechler 12:23
It's not part of your application, so to say. It's part of the infrastructure, right? And that is it's more easy for you because then it's part of the infrastructure and you do not have to care about it. It's a configuration and setup thing, but there is something, for example, Christoph can help you with.

Khoi Nguyen Pham 12:27
Oh.
Yeah.

Martin Kuechler 12:43
If if if that is the case, but you still have logically you still have this one database right? And and then you can have the thing you talked about, so a better read performance and but you don't have the overhead of of all this logical stuff within your application, so that would.

Khoi Nguyen Pham 13:01
Hmm.

Martin Kuechler 13:03
Be a good, uh, compromise, I would say.

Khoi Nguyen Pham 13:08
Uh, to this point I have, um, I just think about it. The way Christophe set up our production is that he set up two separated SQL server.
So not not not just one to separate SQL server. One is the master and one is the one is the slave DB and the slave DB is a configuration as a failover for the master.

Martin Kuechler 13:21
Mhm.
Mhm.

Khoi Nguyen Pham 13:36
But what you are saying is absolutely right. I think I need to check again because the Azure SQL they have multi reason capability already, so we don't need to separate the SQL server instance, we just need one.

Martin Kuechler 13:51
Mm.

Khoi Nguyen Pham 13:52
But we can make that one multi regional.
So we can reduce one.
Then why he would create another one? Maybe just for the backup when the entire first one go down, but he decide to put it in another region. This one I need to check with him again, yeah.

Martin Kuechler 14:07
Mm.
And if something that's a little bit related or it is related to that and and maybe it could help you with the stuff we we talked last time about that so that you have some of your forms or or your pages, your detailed pages that they do.
A lot of lookups, right? We said we talked about that. So just to keep it simple, we have a database and then you have like different fields and they all and some of them have their data locally stored, some not. And then you do those calls and that can take.

Khoi Nguyen Pham 14:36
Yeah.

Martin Kuechler 14:54
Take a while. I haven't looked into that. When you said that they're cached in the UI, does it mean they're cached like in local storage or in the local local storage?

Khoi Nguyen Pham 15:05
Correct, correct. There will be cash in the local store, yeah.

Martin Kuechler 15:09
OK, that's good. So with that I would local storage. OK, with that we we could suggest something conceptually that's is is is like a in the spirit of CQRS.
So we have the problem. Some some of the data is in a local storage, some is not and then we have to those calls. Now you can have different ways of handling that. One idea for I would say more or less simple applications would be to to combine.
Combine everything. Oh, sorry, arrow to combine all those calls into one call, right? So that you take those and you put them all in the same call. So you would you would generate a query that says I need info for field AB and C.
And give me that and so a more dynamic aggregation of the data from from the database so that you you don't have many calls, you have just one call with many fields or or yeah, something like that. So this would be.
One way of of handling this, I think it's quite a simple way, so it could be an idea. But in the other case we could or this would be idea #1, let's say let's let's put it here as.
Uh, one.
Um.
Idea #2 would be to load all the data beforehand. So if if the user starts up for the first time, maybe logs in or something like that, then then you.
Could get all the data that all look up data that he needs and put it into the local storage or look up data. I have applications that's run like that and it's.

Khoi Nguyen Pham 17:12
Mhm.

Martin Kuechler 17:13
That is quite simple because I I don't you have to say if it's if it's feasible or not, but we have experience with applications where you have like only I would say dozens, maybe low hundreds of of data points for master data.

Khoi Nguyen Pham 17:20
Mm.

Martin Kuechler 17:33
We load everything into the client and and then the the the individual pages are quite fast and you can load this as one call at at at the start of of one application and local storage and and the clients easily can easily handle that if it's.

Khoi Nguyen Pham 17:36
Hmm.
Hmm.
Good.

Martin Kuechler 17:53
In the hundreds, even thousands, thousands of data points. And then of course you you would need some thinking mechanism and that would be like remembering OK when when was the last time I.
I um.
I I looked up the master data and then uh OK, ask the server and it says no, we have a new version and then uh we update.
Master data, but we only update for like a small amount of of data points, right? And you could even change that and this would be the CQRS way, a little bit more complicated, but you could even change that to a push model.

Khoi Nguyen Pham 18:34
Mhm.

Martin Kuechler 18:44
That you do you push when when the UI like does a command on the back end as as part of that process you could push an update with with.
Now you already have that with what's called Signalr, right? Signalr into the UI and and so it would be kind of instant if it's needed. I I don't see it to be honest. I think it would be enough.

Khoi Nguyen Pham 19:04
Yeah.
Mm-hmm.

Martin Kuechler 19:16
To to check like master data when you start the application and and from time to time or when you enter a specific page where you need some master data where it could be checked again. But the normal case would be then that you have like.
Uh, always nearly everything in the clients and it it would like be instant. All those look at fields would be instant.

Khoi Nguyen Pham 19:41
Yeah.

Martin Kuechler 19:42
You you you it's kind of like CQRS where you put the um the the the view database into the client.

Khoi Nguyen Pham 19:49
Hmm.
I agree. So from my point of view, our master data, they are not going to change frequently I would say. So user information not going to change most frequently for information also office vessel could be.

Martin Kuechler 20:00
Mhm.

Khoi Nguyen Pham 20:10
But most of the master data is not going to change. The the only thing that I am a bit reluctant on putting every master data on the first load is that there are some master data to consist a lot of record including the port.
The port information could easily reach 10,000 record of port information, so if we could manage to have that mechanism.

20:34
OK.

Khoi Nguyen Pham 20:38
Work uh seamlessly during the first lot of the application. I think it's.
This is fine if we could think of a way to do that and the signal are to push the update to the client also. I think it's a nice idea.
The uh, what I have a discussion with them is that um.
Mostly related to the first option that you have here. So let's say we have like a big detail record to be pushed to the client as the option number one you have. Let's say it is a shipment and in the shipment there could be a user create ID, an office ID and vessel.
ID and a port ID for example. And if we wanted to bring everything into one query, there are basically two ways. The 1st way is that we do a join on the database level, so the shipment needed to join with other table and then bring on up the.
Name and code of the other table as metadata to the main record and push it. So we have only one request but as a trade off there will be a big showing query in the database.
The second way is what I am currently doing right now is that we just send the main record and all of the ID when it reach the component in the front end they will have their own way of handling how that ID will get display.
So if the ID it will try to look up for the local storage. If the ID has not been loaded before, it will call another get detail to the DB to get the port information detail.
And that can also end U in a port ID, port name, port code and country code, country flag, a lot of other stuff and thus the component is much richer. We can handle how the component will display the information just.
By having a simple blog ID and that mechanism is cached in the client before it's sent to the back end. But eventually when we when we go to like roduction and a lot of component can request.
A lot of different master data at the same time and because the client is first loading the application so one of the cache is not there and it end up in a very a lot of requests to the system at that time.
So I think it's that the the cache on the client is not enough. I in my head I wanted to have another cache layer in the in the DB, so maybe a reduce cache to handle all of that query.

Martin Kuechler 23:20
Mhm.

Khoi Nguyen Pham 23:37
That is what I'm thinking about and another way that I'm thinking about is that we do normalization on the on the data. So in the main record we can also do a lot of normalization of all of the.

Martin Kuechler 23:39
Hmm.
Mhm.

Khoi Nguyen Pham 23:53
Related data to it, but it end up in a lot of fields, in a lot of tables that we needed to manage. If the main DB, if the main record change, we needed to look up for all of the normalized data in another table to also update. It's quite expensive for me.

Martin Kuechler 24:08
Mm mm.

Khoi Nguyen Pham 24:13
Yeah.

Martin Kuechler 24:13
Yeah, I I I don't see this this normalization of the of the database. I I don't really see uh a lot of use for the.
From the performance point of view, I I would keep the database uh structure.

Khoi Nguyen Pham 24:30
I I think Nam has a good point about normalization is that when he needed to perform like invoicing things, so he needed to somehow snapshot the entire data at that specific point and to deliver it to the PDF.

Martin Kuechler 24:35
Yeah.
Hmm.

Khoi Nguyen Pham 24:49
So if there's just like an office ID for example, and then it exported to the PDF, then the current office name, current office telephone needed to stay the same in that PDF in that PDF. So normalization in that case it work.

Martin Kuechler 25:06
Yeah.

Khoi Nguyen Pham 25:07
But for not, not for many other cases that we don't want it to end up in having duplicated data everywhere.

Martin Kuechler 25:17
Yeah, right, right. If if you have data that's where where the lookup kind of doesn't is not allowed to change, then of course you you should put it in in in the table in the row.

Khoi Nguyen Pham 25:26
Mhm.

Martin Kuechler 25:32
Yeah, I mean also there you can have different ways of doing that. Like for example, let's let's say we have this is.

Khoi Nguyen Pham 25:34
Mhm.

Martin Kuechler 25:43
This this is like a orders table orders orders. Let me do it other orders.

Khoi Nguyen Pham 25:49
Mm-hmm. Yeah.

Martin Kuechler 25:56
Table then of course you you could have something like so it has ID and number and whatever and dates but but we we have like a a a look up look up like.
Some ID for example and then of course you could you could put customer name in there. This this this would be like.
Normally you wouldn't do it but but but if if the name changes but but the order should stay the same then we would need to put it here so it doesn't change right because of the look up. So this could be its own field.

Khoi Nguyen Pham 26:36
Yeah, correct. Yeah.

Martin Kuechler 26:42
Or if if it's not that relevant to querying, most cases it is it's not you. You could do something like like a Jason. I would call it look up data field.
And just put one kind of BLOB in that row with all the look up data because you don't want to change it. So so you write it once and then it's it's only relevant when you like render this for for an invoice or something then you can can take it out of there and then use all this look up data. So so it would be.

Khoi Nguyen Pham 27:15
Mm.

Martin Kuechler 27:18
Compromised and you you keep your tables like tidy, but you have one field that that that does the that holds all the look up data.

Khoi Nguyen Pham 27:25
Mhm.
OK, understand. Yeah. Mm-hmm.

Martin Kuechler 27:28
Could be an idea.
Yeah. And the other thing I I would say so, so we talked about the problem that you have a lot of calls now here from the UI and then also you have the calls here to the database. So and and that there's like of course that that adds up in in time.

Khoi Nguyen Pham 27:45
Yeah, correct.

Martin Kuechler 27:51
So my idea would be like collecting the fields in the UI and then then you can, yeah, it's it's a little bit a matter of benchmarking I would say.
Is it OK to call then the database multiple times to keep it simple or to create one fancy SQL call where where you have all the data? Or maybe that the better idea would be to cache the the master data?

Khoi Nguyen Pham 28:11
Mhm.

Martin Kuechler 28:21
Next to the API so that you have don't have the round trip to the database. And this could be like, yeah, as you said, we could, we could do Redis or what's even really good nowadays, it's SQLite.

Khoi Nguyen Pham 28:36
Yeah.

Martin Kuechler 28:39
Yeah, then you would have one call collecting this here, collecting it from the cache and then yeah, given it as one package to the UI, it would dramatically.
Reduce the number of round trips that that should be quite faster.

Khoi Nguyen Pham 29:02
Mhm.
Yeah.
I would think that combining several requests in in the controller and then erform one would be quite challenging.
Um, yeah.

Martin Kuechler 29:16
From the UI to the API or from the API to the database?

Khoi Nguyen Pham 29:21
From the UI to the API because each of the component have their own way of and own way and then when to to make a call right? And the way that the component is fully loaded into the UI could be different.
Could be slightly different. So the request that it took can be millisecond different. So there should be like a good mechanism that can bundle up one of those requests and then perform just one call.

Martin Kuechler 29:41
Uh huh.

Khoi Nguyen Pham 29:56
And then that one call needed to handle like a.
Different query to different tables because master data they can spend across like 20 tables easily, yeah.

Martin Kuechler 30:10
Hmm.
Yeah, so this simplest way of course would be something like having a string array and then like like calling.
Vessels.

Khoi Nguyen Pham 30:35
Yeah.

Martin Kuechler 30:37
So and then giving giving this to the to the back end and to the API and it pulls it apart and puts the stuff out of out of the cache right?

Khoi Nguyen Pham 30:48
Mm-hmm.

Martin Kuechler 30:50
Um, yeah. If the components are independent, yeah, it's, it's, it's a bit of a.
I mean, it's good. Yeah, it's, it's, it's flexible, but but this makes more complicated to to collect something like that, yeah.

Khoi Nguyen Pham 31:02
On Yeah. Oh.
Yeah.
But it's is a nice idea that we would like to spend some thought on it. Maybe there could there could be a good way to to handle it, but I just don't know yet. But the the catching on the redis or the SQL line I think could solve the.

Martin Kuechler 31:24
Mm-hmm.

Khoi Nguyen Pham 31:31
Could solve the problem even. I don't think it is even now a problem for the production environment because just 200 people working at the same time and our back end our database is multi region availability.

Martin Kuechler 31:40
Mm.

Khoi Nguyen Pham 31:48
So I think that it also reduce the stress on a single instant of the back end or a single instant of the database already, but at least I wanted to have some yeah kind of solution in the head before the actual.

Martin Kuechler 31:56
Yeah.

Khoi Nguyen Pham 32:04
Traffic jam happened. Something like that, yeah.

Martin Kuechler 32:05
Yeah, sure, sure. And maybe you can already. Um.
Like take a lot of pressure off the system with with like preloading a lot of stuff.

Khoi Nguyen Pham 32:18
Yeah, yeah. Preloading is also nice. Yeah.

Martin Kuechler 32:19
Right.
If if you have like 8090% of the data preloaded, then maybe you cut all those those those tiny calls. Maybe you cut those by a significant number and then it's fine again.

Khoi Nguyen Pham 32:32
Mm-hmm.
Yeah.
OK. Thank you very much.

Martin Kuechler 32:44
Yeah, no problem. What? What do you think would would be for a next meeting? Something something good to prepare?

Khoi Nguyen Pham 32:45
Mm-hmm.
The next topic I would talk about is that I think I needed to to to involve Nam in the next meeting also because it's mostly related to the stuff that I think he will he will need.

Martin Kuechler 33:09
Mhm.

Khoi Nguyen Pham 33:16
For me, I think that we need to have like a very good way to handle those background task, a heavy background task, most likely to export and import data from BDF during during a voyage, because during a voyage every day there is a lot of.

Martin Kuechler 33:22
Mhm.

Khoi Nguyen Pham 33:36
Of invoicing BDF coming out and coming into the system and it needed to read and write continuously. So I think that one is kind of challenging, but this may be on on on park more than miles parked.

Martin Kuechler 33:44
Hmm.
OK. I will give it a little bit of thought and maybe also talk to Christoph about that because we already talked about that a little bit and I think this is also a good topic for something like.

Khoi Nguyen Pham 33:54
Yeah.

Martin Kuechler 34:10
Azure function calls or something like that.

Khoi Nguyen Pham 34:15
Answer function, yeah.

Martin Kuechler 34:17
Yeah, it could be because they have to scaling right then then you have to do not have to worry about the the infrastructure part. But I I I will give it give it a little bit more thought maybe I will write num and and ask about.

Khoi Nguyen Pham 34:20
Mhm.

Martin Kuechler 34:34
Or or or maybe if if you have a minute some in the next days just the amount of data and and maybe the time of computing you have like normally if like like just just a as a a gross measure like it takes a minute.

Khoi Nguyen Pham 34:52
Mhm.

Martin Kuechler 34:53
On my computer or or something like that, right? Just just just I can have a little bit of an image of of what we're talking about or if it's like 10 minutes or an hour or something like that, right? With gigabytes of data.

Khoi Nguyen Pham 34:57
Mhm.

Martin Kuechler 35:10
So that that would be interesting, yeah. And and then just a small problem, I will be on vacation in two weeks time from from now on so.

Khoi Nguyen Pham 35:25
Mhm.

Martin Kuechler 35:27
I would suggest the 16th or the 17th, so next so in one week, the Thursday or or Friday, but I'm also still there Monday the 20th and the 21st Tuesday.

Khoi Nguyen Pham 35:32
Yeah.

Martin Kuechler 35:42
Would be the last chance that that we could talk and then I'm on vacation for about two to three, two to three weeks. Yeah, three weeks. Yeah, I I I will. I will write you those dates again and then you just tell me what what what's what's what's good for you, right.

Khoi Nguyen Pham 35:50
Mhm, mhm.
Yeah.
Yeah.
OK, I think this makes sense.

Martin Kuechler 36:04
All right, great. Yeah. Don't hesitate if you have any questions for for the stuff we talked about or other stuff. Yeah, I'm, I'm here to help if you have something. So just drop me a message and I will answer by mail or or in in chat and or we could have another call, right.

Khoi Nguyen Pham 36:09
Mhm.
Mm-hmm.
Yeah, Martin, if it's possible, then I also wanted to ask your opinion on one thing that currently Nam and me have a discussion on. Maybe, yeah, another topic that just arrived in my head.

Martin Kuechler 36:38
Yeah.

Khoi Nguyen Pham 36:42
Is that the now want to have like to to apply a global query filter to apply for all of the record that is being used with.
Yeah, so a bit of context on that is that our system supports soft delete, but not on every record. There are some record that we needed to hard delete, but the the soft delete record now apply for the master data.

Martin Kuechler 37:06
Mhm.
Mm.

Khoi Nguyen Pham 37:16
And also for the invoicing that Nam is working on.

Martin Kuechler 37:19
Mhm.

Khoi Nguyen Pham 37:20
And during the the work on the invoicing NAM encounter that the developer, they usually forgot to query out the data that has been soft deleted because they needed to include another where.
Record dot dot is deleted equal to four something like that, but sometimes that they just forgot so they asked. So now I'm ask another developer to like write an auto and global query.

Martin Kuechler 37:41
Mhm, mhm.

Khoi Nguyen Pham 37:53
Into the data context that every time they call a context dot some table, it automatically alley the sub delete.
Uh preview to the record and for me I have a discussion with them in like 45 minute very tense one and because I for me that system is designed that from the start it is not using sub delete as a default.
So all of the code up from the start to now already have that in mind that they always query for the entire data and then they can do hot delete when they needed to. But now if we apply that filter even though it's just like some line of code.

Martin Kuechler 38:27
Hmm.
M.

Khoi Nguyen Pham 38:40
But if it if I apply it to the system, it would end up in that the entire application we needed to retest and all of the places that we we have to revise on whether or not it would end up in the bug that we.
We don't know Nam. Yeah, Nam has a good Nam is very smart and quick, but he could identify quickly where could be the problem and that is a good thing. But to me it is still not enough because I still feel unsafe about it. So I insist that that way we don't do it.

Martin Kuechler 38:57
Hmm.
Mhm.

Khoi Nguyen Pham 39:15
We should having another separated like sub query and then sub include instead of applying that global query directly to the main DB. So we have quite an intense discussion on that.

Martin Kuechler 39:31
Yeah.

Khoi Nguyen Pham 39:31
So yeah.

Martin Kuechler 39:33
I I I see your point. Yeah. If you have or yeah, other way around, if you don't have exhaustive tests, and I think you don't have them at the moment, I would be really cautious.

Khoi Nguyen Pham 39:49
Mhm.

Martin Kuechler 39:53
With a change like that, because you like changing everything, right? And if you don't have a good battery of of automated tests that then checks that you don't have any regressions, it is dangerous.

Khoi Nguyen Pham 39:55
Yeah.
Mhm.

Martin Kuechler 40:09
Right. So that would would would speak against it and I'm also but this is the personal way for me but it it's it's it the time showed me that it's it's good idea to have.

Khoi Nguyen Pham 40:09
Mm-hmm. Yeah.
Yeah.
Yeah, got it.
Mhm.

Martin Kuechler 40:37
Entity Entity Framework context and it does stuff and and I'm even not a fan of Entity Framework. It's it's good for some stuff, but for example it's very good for creating code first your database.

Khoi Nguyen Pham 40:40
Mhm.
Hmm.

Martin Kuechler 40:51
First, your database. But I don't like the queries. I don't like the magic of including other stuff, so I I would write that by hand. Um.

Khoi Nguyen Pham 40:56
OK.
Yeah.

Martin Kuechler 41:03
So for me personally, it's magic. I don't like it.

Khoi Nguyen Pham 41:07
OK.

Martin Kuechler 41:09
Yeah, but yeah, I I understand this point, but I would write down the cases where where you where you definitely have to filter out the the soft deleted data and then go through the code and change it and make it explicit that you filter out.

Khoi Nguyen Pham 41:10
Thank you very much. Yeah. OK.
Hmm.

Martin Kuechler 41:27
Uh, the soft deleted data.

Khoi Nguyen Pham 41:30
Yeah, yeah.
I also like it to be very clear in the code that I only want to query out a filter query. It should be like soft query and then if I want to include the children data that also have soft delete I would.

Martin Kuechler 41:37
Yeah.

Khoi Nguyen Pham 41:47
Rather see it as sub include instead of include, but the sub include we needed to to write customly, but at least it's make the code cleaner when we read it back again.

Martin Kuechler 41:58
Yeah.
Yeah, yeah, often. I mean in in our projects is I guess it's more often the case than in your project that we have like new people coming on and that's why I'm always a bit extreme because I I have a lot of new people always who are new code new.

Khoi Nguyen Pham 42:02
OK. I think that's, yeah.
Um.

Martin Kuechler 42:22
Stuff. So I have this extreme stamp out. I said it keep it really really really simple. No magic if it's in any way possible because someone will join and look at the code and think what is happening, why do I get do not get the data or something like that and.

Khoi Nguyen Pham 42:28
Yeah.
Yeah, yeah, mhm.

Martin Kuechler 42:38
So.

Khoi Nguyen Pham 42:40
OK, got that. OK then. Thank you, Martin. I think for the next topic we needed to to get now involved to see what is the pinpoint on his side and then we schedule for the next one with you.

Martin Kuechler 42:41
Yeah.
Yeah.
Yeah.
Yeah, I will write in the in the teams chat just a summary for Nam and and for you with the dates and topics and stuff like that. And then yeah, you can just tell me when when it's fine for you, right?

Khoi Nguyen Pham 42:56
Yeah.
Yeah.
Mhm.
Yes.
Yeah, would be perfect. Thank you.

Martin Kuechler 43:12
All right then. Yep. Thank you. Have a nice day.

Khoi Nguyen Pham 43:13
OK.

Khoi Nguyen Pham stopped transcription
