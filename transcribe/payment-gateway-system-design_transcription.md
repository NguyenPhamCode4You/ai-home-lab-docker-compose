# Video Transcription

## Summary
This document contains the transcription of the provided video file.

## Content

Transcription with Segment Timestamps:
[00:00 - 00:15] Hello everyone, my name is Huy Tran Quoc Huy. In my entire career, I have been in the field

[00:15 - 00:30] It is my favorite field. My favorite database is all over the country. All over the system from securities, banks, telecommunications. In and out of the country, I have it all. Sitting here with you guys, sharing with me today, there is a friend Trung and a friend Dinh.

[00:30 - 00:45] two brothers and sisters who are students in my program Wecomix 100x. Actually, it's just called a student, but their work is also very good, very good. My mindset when organizing these sessions What is it? It's me, it's the brothers and sisters in my community, the Wecomix community 100x, then we share

[00:45 - 01:00] Hello everyone, my name is Trung.

[01:00 - 01:15] I have about 15 years of experience and currently I am in the role of backend technical lead. Hello everyone, my name is Dinh. I am a backend developer. I specialize in Node.js and Cloud in the cloud industry.

[01:15 - 01:30] in the field of e-commerce and logistics. I'm very happy to be here today to share a system design with Mr. Huy and Mr. Trung. Hello everyone. I believe that when talking about payment,

[01:30 - 01:45] I think many of you have experienced this. You will see this in many places. For example, now we are going to have breakfast. Most of the money is used to help the phone, scan the QR code, transfer the money and that's it. It's been a long time.

[01:45 - 02:00] I don't have to spend money for breakfast and the payment part actually there are many companies that provide that payment such as international payments such as Paypal or Stripe so every time we pay like that

[02:00 - 02:15] So today, me, Trung and Dinh will sit together and think about it. So if we want to get involved in a company about FinTech and want to make a payment gate, we don't know what to do.

[02:15 - 02:30] How to approach us will be like how we can do the service That payment gate that it designs everything it is called it is less expensive And besides, I want to go through what we share here, you can learn

[02:30 - 02:45] First of all, during this construction process, I will understand the suitable balance of the payment gate in the outside world. Now there is a store that wants to integrate the payment gate, I have to know how the balance is implemented, right?

[02:45 - 03:00] The second thing I want to share here is that in the payment section, there is a payment in our country, the banks transfer money to each other. Ok, we will have a section that shares the balance, you guys scan QR code to keep the banks, I scan the money to transfer to each other.

[03:00 - 03:15] How do you design it? What if I want to use my credit card now? Then I scroll through my credit card My brothers and sisters are a small company We have to work hard How can we do it?

[03:15 - 03:30] We will discuss this content together. And here you can see that this is a big picture of the bank account. In this bank account, on the general face, it will have its units

[03:30 - 03:45] And how do customers interact with those sales units? These are the units called Paypal, Stripe, and those connected to banks are a series of security methods. Everything we will try

[03:45 - 04:00] We will try to exchange in today's session so that you can understand. In general, the payment part, to be honest with you, these systems are definitely not easy. It can't be said that this system is easy. Everything is related to money.

[04:00 - 04:15] It is very complicated and it needs different requirements. In terms of nature, it will include many requirements, such as security requirements, payment methods, how to connect to the bank, how to do business, etc.

[04:15 - 04:30] We will try to use all of these parts, but how to make it compact, how to connect, how to make us be able to start everything in the simplest way. That is our approach.

[04:30 - 04:45] Now, this part will have two main chapters, the first chapter will be decided to share with our brothers and sisters related to now, for example, if you go to eat breakfast, I just went to eat breakfast

[04:45 - 05:00] then I scan the QR code code then behind the story After scanning, what happens behind? After that, I will share with you related to how to give a credit card Ok, listen If you encounter that math

[05:00 - 05:15] How do you approach it? Please share with us. Mr. Huy has already talked about the first part. I would like to go through the payment process quickly. In the process that everyone is going through,

[05:15 - 05:30] um

[05:30 - 05:45] The payment system is used to deal with the transaction, including the accounting bank, which is the bank of the merchant, the network system, such as Visa or Mastercard.

[05:45 - 06:00] and the card issuers. This is a basic framework for how we can handle a transaction. And the transaction also needs to have layers related to security. For example, when we enter the card information,

[06:00 - 06:15] so that we can have more security improvements to enter OTP. This is a loop related to an application card system that transfers money through the credit card network.

[06:15 - 06:30] There is another field that I work in, which is the field of money transfer, electronic cash. It is quite similar to architecture, but the object

[06:30 - 06:45] to deal with the main business. Usually, the units are national payments, or like in the US, it has FEDS or Greenhouse. Returning to the Vietnamese equation, when I want to design

[06:45 - 07:00] in the Queer Code system, the first step would be to refer to the leading unit of the payment solution, that is, VNPay, to understand how they, or just refer to it.

[07:00 - 07:15] or rely on their use case to come up with their own solution. For VNPay, when we go to a cafe or buy a product in a shop, we often have

[07:15 - 07:30] The transaction method is to scan the QR code. After scanning the QR code, the transaction will be carried out through the banking system, especially the banking system

[07:30 - 07:45] NAPAS 247 National Payment Agency to deal with the transfer of money to the bank. What really happens after we scan the QR code is what happens. For a user, a user will have

[07:45 - 08:00] I have a banking application on my mobile app. I will scan a QR code placed on the desktop or send it to a screen.

[08:00 - 08:15] After the query is done, the app will process the information to display on the information and we can actually transfer it immediately.

[08:15 - 08:30] After that, the app will need to be connected to the VNPay gateway to check the information that the QR code provides.

[08:30 - 08:45] to see if it is true. For example, Mui Tran is a different number. After that, the system's task will be to transfer money to one of Mui Tran's banks. This transfer will go through a system called Napa.

[08:45 - 09:00] a central bank, the money will be transferred to the bank of Merchant, and then it will be recorded in the account of Merchant Account. And finally,

[09:00 - 09:15] In the end, we will send the results to the customer to inform them that the payment has been successful. This is a fairly basic balance.

[09:15 - 09:30] completely cover all the actual deposits. However, it will also let everyone imagine the role of the payment cluster here. What is it? And what are the objects in the transaction processing system?

[09:30 - 09:45] including the issuer bank, the merchant bank, as well as the NAPAS system. Here, we understand that VNPay is just a mini VNPay, right? We understand the idea of VNPay, right?

[09:45 - 10:00] I understand what you mean. You said that we will use a bank account. I sent the account of the business owner to use BIEV, right? The gateway is in the middle, right? So now if we are a financial unit,

[10:00 - 10:15] that we want to implement a similar payment gate as VNPay, the first thing we have to realize is that the requirement of the simplest payment gate will require some

[10:15 - 10:30] What is the task? Here, I will list three main pillars that must be available. For example, first, it will provide a payment method. And here, I choose the simplest payment method, which is the QR code. In fact, the QR code

[10:30 - 10:45] There will be two types, one is the fixed code, the other is the mobile code, mobile according to the order. These codes will have to have a standard format so that any app in the bank can scan and get the information.

[10:45 - 11:00] The second requirement is that the real object that we support is the retailers, the merchants. In this case, we need to design a suitable field for the merchants.

[11:00 - 11:15] When a Merchant is onboarding in the system, it needs to set up and provide information for Merchant, such as credentials, API keys, webhooks, and tests.

[11:15 - 11:30] S-Environment. Providing the API to the merchant so they can integrate and process the transaction such as creating the transaction, checking the transaction status or complete the transaction if necessary.

[11:30 - 11:45] webhook endpoint to synchronize the notification via time. And finally, one of the indispensable factors when it comes to security, is how to combine

[11:45 - 12:00] Gateway and Merchant are as safe as possible I also choose some typical items For example, dealing with authentication Encryption via TLS

[12:00 - 12:15] cũng như là việc mình sẽ cần phải mã hóa những dữ liệu để cả set các limit để đảm bảo hệ thống an toàn và cuối cùng trong một cái nghiệp vụ liên quan đến thanh toán thì cái core business của nó chắc chắn

[12:15 - 12:30] will be processing payments, payment processing. We will also have to manage the trading status, checking status, as well as handling HK, cases of unauthorized transactions.

[12:30 - 12:45] For example, in time out, we need to handle tasks related to recharge logic as well as double booking or double transaction.

[12:45 - 13:00] I think that here you guys also understand the main functions and the core business includes money transfer and transaction management and now if you don't transfer the money, you have to return the money to people, right? So now we will discuss together, let's assume that now

[13:00 - 13:15] What is the first step of the implementation and integration? I really want to know that if the implementation is suitable, now you have a business, a store, now you come to implement your webway system, what will it include?

[13:15 - 13:30] How will you implement this Merchant integration? The first step when Merchant wants to integrate our system is that they have to register. For example, a business group enters our system.

[13:30 - 13:45] The first step is how we can confirm them as a business. In this step, we actually need a follow manually. We have to have an admin.

[13:45 - 14:00] from the information of this merchant. After that, they will create an account for the merchant in our network. At this point, the merchant will have an account to use. I think doing this step will help the merchant

[14:00 - 14:15] to ensure the safety of our system. Okay. Once we have the account, the merchant can update the information such as the account to receive money. That is, they want the system to send money to which account for them. Webhook EOL is the information that they want

[14:15 - 14:30] How do we send a notification about their system? Or IP-wide listing? I see some payment systems will use this platform to allow merchants to send requests from a certain IP. And then merchants will send requests

[14:30 - 14:45] will receive some information that they can integrate such as Merchant ID or information about Access Key and Secret Key These information will help Merchant integrate our system in a safe way And besides, because it is very important information

[14:45 - 15:00] I think they only allow you to watch it once. After you watch it, you have to download it and put it somewhere. You have to cut it, right? Yes, and then you can't watch it. Or you can only watch the end part. After you register,

[15:00 - 15:15] After the registration, the first step, the simplest step that the merchant wants to have right away is to have a QR Tink. Sometimes they want to paste it in front of their store so that the user can go there, buy the goods and transfer the money.

[15:15 - 15:30] This QR will contain information such as account number, account name, or bank name. So you may have a question that where will you get the information from in this QR?

[15:30 - 15:45] Merchants will surely have their own accounts in their system. If we use that account to generate this QR code, there will be a problem that we will not be able to track the transactions in their accounts. That is, we don't know the money in their accounts, right?

[15:45 - 16:00] There is a solution. Some banks will allow us to register a special account, Master Account. From this special account, we can create children's accounts,

[16:00 - 16:15] We can use these accounts to map with who this merchant is. After registering the merchant, we will create them a supercal account like this. Actually, the master and supercal topics are quite complicated.

[16:15 - 16:30] I will not go deep into it. I will just leave it like this. And I think we can find banks that have this way to integrate with them. Ok, what is your idea? For example, we have a chain of Long Chau Pharmaceuticals.

[16:30 - 16:45] in different locations, right? So now we will create a chain of accounts of Mr. Long Chau But we need to have a master account so that later the children's accounts can collect the money so that the people above can still know that information, right? Yes, that's right

[16:45 - 17:00] Ok, and we will create Quera from there, right? Yes, because our system will own this account so that we can know exactly how much money comes in and this Quera will be based on the subaccount account. Ok. I keep saying Quera from now on, but I don't want to…

[17:00 - 17:15] Quera has a certain structure. We have two types in our system, Static Quera and Dynamic Quera. Static means we only import the money manually, while Quera means

[17:15 - 17:30] When a merchant wants to create an order with a specific QR code for that order, we will use the dynamic QR code. The structure of a QR code has a common standard.

[17:30 - 17:45] We can research more about this QR code. It's a key value chain. From that key value chain, we can convert it into a QR code. And when the buyers scan that QR code,

[17:45 - 18:00] we can convert it into transferable information. Its structure is quite easy to understand. You can research more when you want to integrate. In addition, creating QR codes,

[18:00 - 18:15] There are many ways to create queries. We can use libraries to create information such as name, bank code or account number. In addition, we can also use SDKs or third-party APIs

[18:15 - 18:30] such as the web site vietqr.vn or nampassopenapi, it is very easy to create queries. The advantage of using API is that it will have a number of information such as we don't need to process checksums,

[18:30 - 18:45] or the bank's logo is also integrated, then the query will be expired easily. Of course, it's easier to use API, but when we want to own our own logic,

[18:45 - 19:00] handle the logic, then the use of a library is also simpler. When we have a static viewer, we can have a follow-up. Some merchants, when they

[19:00 - 19:15] They already have an order, they want the customer to scan the QR code to get the money. Most of them go shopping, scan the QR code and get the money, get the order, right? In fact, that logic will help...

[19:15 - 19:30] It helps a lot of things Firstly, it's easier for customers to transfer money And secondly, it's easier for merchants to manage So what will this flow be like? Merchants will have a server They send me a request To create an order That is, a query

[19:30 - 19:45] In this query, it will include the amount of money and the order ID. After receiving this request, our system will start to check what the sub-account of this merchant is.

[19:45 - 20:00] After creating a WhatsApp account, we will create a note in the database. This note is a transaction and we create it so that the following will be simpler and easier. After creating, we will return the QR information to the merchant.

[20:00 - 20:15] We can use this QR code to transfer money. When creating a QR code, there are some risks like this API will be exposed.

[20:15 - 20:30] like HTTPS or more advanced like SSKey, I see that some systems like Stripe and Paypal all use SSKey to help our API to be more secure.

[20:30 - 20:45] Next, after the user has the QR code, how will it work? For example, the QR code is on a post machine in a store.

[20:45 - 21:00] And the users use the Vietcombank app They want to transfer money to our merchants who are using BIDV When they scan the QR code, the Vietcombank app will pass the money

[21:00 - 21:15] Thank you very much.

[21:15 - 21:30] a third party which is Langpass247 which is a very popular service. After the transfer of money and the user has been confirmed, the bank system will send us a webhook. This webhook

[21:30 - 21:45] It will include the information that the payment status is successful or failed And next are the information such as the sender or the receiver Or the transfer content And we will rely on these information to map into our system

[21:45 - 22:00] to see exactly what the Transaction ID is. Then we will update the status for it to be accurate. After updating the status, we will send webhooks to Merchant Backend so they can have their own tasks at Merchant Backend.

[22:00 - 22:15] They want to receive this notification. The information can be successful or failed payment, and information about what the order is, or how much the amount of money is. When this flow is done, the money is being transferred

[22:15 - 22:30] is still in our system. That is, it is in Merchant's subaccount. When will the money in this subaccount be transferred to Merchant Bank? In my opinion, when we first designed it, to make it safe,

[22:30 - 22:45] that we will not pay the money immediately for the merchant that we will leave for 1-2 days so that we can reverse the transaction in this database and in the master account that we own to see if that transaction is legal or not.

[22:45 - 23:00] then we start to send money back to the merchant. Okay, according to this chart, according to what I see, this chart will have at least the database part. Earlier, we had to insert the database, and when we inserted it into the database,

[23:00 - 23:15] database, then you will have to continuously update the status status of that record, right? Yes, that's right. And in this field, this database will have to serve, in addition to performing

[23:15 - 23:30] It also has to perform transaction monitoring, that is, it will run reports, select, check track, etc. If many of them run at the same time, in principle, the database may be contention.

[23:30 - 23:45] Yes, exactly. The database can have problems in this part. In part 5, there will be some problems that we need to implement more detail because it is possible that sending requests from VNPay,

[23:45 - 24:00] and send it to Merchant Backend, what if there's an error on the way? At this point, we will add a queue in the middle to receive the events from the VNPay system. These are the events where the transfer of money has been successful. Okay.

[24:00 - 24:15] We will have another worker to receive the event from here Then we will shoot the request for Merchant's webhook The information I will include is the amount of money, order ID, information that

[24:15 - 24:30] Merchants can use it to verify the order for them. In addition, we need to add an item button key. It is in the case that we avoid the case that we send an event twice. Merchants will be able to handle it. This item button key can be built based on

[24:30 - 24:45] such as event ID, order ID, or sometimes the banking system will send along with the item button key that we can also use. In addition, we also need a way for merchants to verify this request.

[24:45 - 25:00] coming from our own system, not from another system that is being utilized. We will add the access key or the signature. This signature will be built based on the payload that we send.

[25:00 - 25:15] and a secret key that we digitized here. After the worker sends this request to the merchant, it can be based on this payload, and there is a public key to verify that this request is accurate from the merchant's side.

[25:15 - 25:30] Besides, it also helps us to retry our mistakes whenever we send them. Or we can save them somewhere when they all go wrong. Okay, this is the mindset.

[25:30 - 25:45] At least in the process of sending it, you have to save it somewhere, right? You have to ask for something, right? In the case of sending a SIM card, there is an opportunity to send it back to you or someone else, right? Yes, exactly like that. Ok, you guys have gone through a loop, now the loop is related to money transfer, right?

[25:45 - 26:00] How do you deal with the payment system? Payment system can be derived from many causes. For example, merchants want to pay their customers back.

[26:00 - 26:15] Or sometimes the bank system sends us a webhook and we check that this transaction has been successfully paid. Then there is a rare transaction where the customer transfers money twice and it will happen.

[26:15 - 26:30] We have to refund it to the user. To start this refund, we will first save the refund in the database. Then we can check, we can monitor its status. Next, we will send it to the user.

[26:30 - 26:45] send an event refund in the queue. The information will be similar to this. We include information about the account, information about the status, information about the order ID. Then we will have a separate worker

[26:45 - 27:00] and I will refund it to the user's account. I will refund it until it is successful. After the refund, I will update this record so that the merchant can follow it.

[27:00 - 27:15] According to my understanding, when we have information in this database, we have a lot of ways to do it. For example, in this case, we have a box of goods, we have to re-fund all of them. Or as you said, it sends a loop to the customer.

[27:15 - 27:30] I don't know. I don't know. I don't know. I don't know. I don't know. I don't know. I don't know. I don't know. I don't know. I don't know. I don't know. I don't know. I don't know. I don't know. I don't know.

[27:30 - 27:45] They have to actively create a refund for the customer. Then our system has to find the information of the customer. That is, the customer does not have to send the account number to you. Because all the digital information is sent to the customer.

[27:45 - 28:00] I saved the amount of money in the database at the beginning of the transaction. This system will check all the money in the database. You transfer the money to me from which information? If you send me 100,000 VND, I will pay 80,000 VND.

[28:00 - 28:15] You can update that I have about 80,000 VND in my database, right? Yes, we can know the information in the transaction because we have saved all this information. When we refund once, we will add information about the amount of money here.

[28:15 - 28:30] to be able to refund the exact amount of money for the user. Okay. After I've done the refund, I think I have a follow-up for the QR payment, which is the QR code.

[28:30 - 28:45] How will the user transfer money to the merchant? How will I handle the refund? How will the performance be? We will have a general architecture for the entire project.

[28:45 - 29:00] I think Trung will be able to analyze the architecture overview in more detail. In the previous episode, Mr. Huy also shared with us how we can partition the database.

[29:00 - 29:15] to solve problems related to efficiency, I will also share a little bit, add a small point before I explain this part. That is, if I partition according to what criteria to ensure balance, then I will usually choose

[29:15 - 29:30] The first two criteria are based on the machine ID, the second is based on the time. Then there are questions related to this system, in the transaction processing field, does it need queue, does it need reddit, does it need login?

[29:30 - 29:45] The answer is that everything can be applied to this field. However, to simplify it so that people can understand the field, in the presentation, it gradually goes to that field.

[29:45 - 30:00] In general design, we can apply those components in the transaction processing stage. For example, credit can separate the closest transactions because the status of a stock exchange is quite fast.

[30:00 - 30:15] to verify the information. We can also use the message queue to route and process in a scale. For example, different Merchants can be routed

[30:15 - 30:30] and different partitions in order to use the size that we handle. Then, the file log parts. In the system, any component can be shared. Although we have a good database design, we can design well

[30:30 - 30:45] there is still a possibility that the system will die. Therefore, we will always save the layers and save the letters on all the instance and object stores to ensure.

[30:45 - 31:00] When we have an accident, we will always ensure the ability to restore the system. In this overview architecture, we have separated into layers and components so that people can easily follow. People can see the overall architecture.

[31:00 - 31:15] First, it is the objects outside the system, such as Merchant, Bank, or NAPAT247 system. When we design a system related to the final payment,

[31:15 - 31:30] One of the most important elements of the gateway is the security and security of the system. Therefore, I will design a layer called API Gateway Layer for all external communication.

[31:30 - 31:45] In here, I will try to design how to have components such as API Gateway API Gateway will help me easily integrate security, firewall

[31:45 - 32:00] then routing to the services I will also add the Authentication AuthService in this layer as well as the general ready-mix of the entire system I can set up ready-mix for

[32:00 - 32:15] But for this system, we should set up the entire layer to ensure that if a Merchant or a third party, when they meet, they make mistakes.

[32:15 - 32:30] The error that leads to the DDoS system will not affect other machines. This data will be routed through the load balancer to the core services that we handle.

[32:30 - 32:45] In terms of length, we will design it according to the Microservice model So we can temporarily divide it into small pieces for everyone to use If we design the Microservice, how will we design it? For example, we can divide it into Payment Service, Notification, Refund and Webhook

[32:45 - 33:00] Core-Civic layers will be deployed in a VPC cluster to ensure that its network is as safe as possible. Next is the layer related to data layer.

[33:00 - 33:15] such as message queue and database as well as object storage where the backup files are stored In the programming related to the design

[33:15 - 33:30] payment gateway system, we need to ensure that the system will be stable and the time it serves is almost 99.99%. As of yesterday, you can see that

[33:30 - 33:45] When AWS died, there was an accident. All the platforms that were deployed on AWS were affected. However, there were some platforms that were slow. But there were some platforms

[33:45 - 34:00] It will depend on how they implement the system to prevent such severe accidents. I can give you an example.

[34:00 - 34:15] It was when we implemented the entire infrastructure on a data center in Hanoi. But one day it was flooded and the data center was outstaged and our service could not work.

[34:15 - 34:30] to our main task. If we deploy on AWS, then one day AWS will also face an accident in a region and the service will also be affected. So how to minimize

[34:30 - 34:45] It comes from the design mindset. I want to share a little bit about my point of view when looking at this overall architecture. First of all, I like the fact that we will divide our system into many parts.

[34:45 - 35:00] In fact, according to Mr. Tu Duy, when I do the project I love, I actually have a lot of secrets that I love. Among them, one of my favorite secrets is that when I come in, I always know that in my favorite job, it contains 30 ingredients. That is one of the most important things.

[35:00 - 35:15] This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it. This is the way I usually look at it.

[35:15 - 35:30] I was affected by the load manager, I was affected by my core service including money transfer or webhook service or refund Or I was affected by layers of database. When we see layers like that

[35:30 - 35:45] If the customer's calculation requires high accuracy, then it must be clear that each buyer must have high accuracy. That means we have to put it at least double-checked to be safe or to be broken in two different areas, two different houses.

[35:45 - 36:00] This is how I look at this architecture and what I think about it. And in this architecture, we only see some of the banks and the transfer of NAPAT 247 money. This is just a part of the story.

[36:00 - 36:15] In the future, our architecture will have to face more calculations. So how about the transfer of the credit card? Now let's talk about the credit card. Can you share with us? First of all, through the overview architecture,

[36:15 - 36:30] With a payment gate, we have basically designed a simple method, which is to use QR code. However, with a payment gate, there is usually not only one method.

[36:30 - 36:45] and it will have to integrate many other methods such as credit card, and more, such as digital passwords, etc. In this integration, I will choose the password

[36:45 - 37:00] is more suitable for the application. So, what kind of payment gateway will it need? It will have to connect to the banking machines through credit card networks to ensure

[37:00 - 37:15] is that these transactions are successfully carried out. Secondly, when we work with the credit card system, we also need to pay attention to one standard, that is the PCI DS of the security standard.

[37:15 - 37:30] And thirdly, it is the task of the application card, that is, for the application card, when we use the application card, we will also have to understand how this system is designed.

[37:30 - 37:45] it will design its mission, including many steps. Here, I can list four basic steps. First is Authorize, which is a step that will be

[37:45 - 38:00] Giữ duyệt và giữ tiền của khách hàng Bước thứ hai gọi là capture Nghĩa là thực hiện cái việc thanh toán Bước thứ ba gọi là settlement Nghĩa là cái giao dịch này Nó đã được kiểm định Tối soát thành công Và cái việc chuyển tiền nó đã thực sự diễn ra

[38:00 - 38:15] and finally it is related to the refund then below there is a more detailed flow so that everyone understands that a transaction through the credit card will include some steps a full follow for example like

[38:15 - 38:30] When we buy goods on an e-commerce site, after we buy goods, we will need to enter more OTP codes. Here it is a layer called 3DS.

[38:30 - 38:45] authentication after it has been approved the bank will issue for example, we issue a card on Vietcombank Vietcombank will keep a

[38:45 - 39:00] and we will not be able to use that money. This step is called Authorize. After this step, it will come to a step called Capture. This is the step where the transaction is actually done.

[39:00 - 39:15] After this step is completed, the credit card system and the banks will handle the transaction and notify the bank.

[39:15 - 39:30] and we know that the transaction was successful. In credit card systems, there are two payment mechanisms. The first payment mechanism is Void, which means that it completely destroys and does not waste the transaction.

[39:30 - 39:45] When we buy a Shopee account and we see that we have bought the wrong one, we can completely destroy it and it will not lose any fee. Because this transaction has not really taken place on the credit card system.

[39:45 - 40:00] but it only works on the bank, it only needs to unlock this currency. However, if this transaction is completed, our currency will go through another loop.

[40:00 - 40:15] It's called a refund. In this loan, there is a mechanism to repay one part or the whole amount. Even when we repay the whole amount, the amount that we want to repay

[40:15 - 40:30] for the user we will still have to pay the fee and this fee we will have to pay or we will have to pay if they want to pay completely for the customer Actually, we have to pay for the customer to pay, right? Yes Then

[40:30 - 40:45] In order to design a credit card system that requires high security and safety standards, what was your first thought when designing the system? Now I am a teacher.

[40:45 - 41:00] How do you approach the application? From the beginning to the end, how can we do it? In fact, for us to be a unit that can be integrated into the application,

[41:00 - 41:15] The credit card system, such as Visa and Mastercard, requires us to meet a lot of safety and security requirements, as well as asking for permission from the government to transfer money.

[41:15 - 41:30] Therefore, in the short term, we will focus on the technical and practical tasks of transferring money through another payment provider.

[41:30 - 41:45] have completed the audit process, have been paid, transferred, and so on. It will help us to quickly implement this feature. However, we will limit one point, which is that it is very difficult for us to calculate fees for people

[41:45 - 42:00] Because the fees on the other side have been quite high. So what is the design of this card slot? For a user who uses a credit card, they will enter the card information into the card slot.

[42:00 - 42:15] However, this card information will not be allowed to be stored in the raw form, but it will be forced to carry out a process called tokenization. This process will code the card information.

[42:15 - 42:30] And before it can be sent to the partners to handle it, what will we prioritize to handle our system?

[42:30 - 42:45] the core payment processor. Secondly, we need to handle the tasks related to tokenized. We need to manage the tasks that we want to enable in the security layer. And finally, we need to

[42:45 - 43:00] to build related to monitoring and audit. This is the scope that we want to implement in this project. Ok, that means I only do a few parts. I audit logs, I verify something, right? The other part I send to the third partner.

[43:00 - 43:15] OK. OK, uncle. This is a strategy that we will apply in the short term. And in the long term, when we have asked for permission, we have qualified the standards of the government.

[43:15 - 43:30] For Visa and Mastercard, we can fully implement it. Here, we can see that you have to keep very sensitive information, such as card information. There are standards and standards of the payment system for card information.

[43:30 - 43:45] so that we can know what kind of standard it needs to do that. So that we can know the existence of it. When we make a payment, one of the extremely important standards that almost everyone has to pay attention to is PCI DSS. That is Payment Card Industry.

[43:45 - 44:00] data security standards. This is the mandatory security standard of all organizations that want to save and transfer data related to payment data. PCI DS has 6 main groups. One is

[44:00 - 44:15] The second requirement is to protect the data of the card holder. The card holder data, such as the card code of the card holder and the card holder of the card holder. The second requirement is to protect the data of the card holder, such as the card holder data, such as the card holder of the card holder and the card holder of the card holder.

[44:15 - 44:30] and so on will need to be tokenized and not allowed to be stored in the database The system will also require the management of the security networks to check the rights, control and control

[44:30 - 44:45] In fact, when we implement it, there are many levels for us to raise the standards of PCI. Instead of trying to

[44:45 - 45:00] When we do everything, we will focus on the most important factors that we can control in the beginning, including how to virtualize the card. I will share a little bit here. At PCI DSS, I also make some database for my customers to meet the standard.

[45:00 - 45:15] This is one of the things that I usually apply. I told the story to my brothers and sisters that some of them will need to have a dataway. Normally, it is called ClearTech, that is, which customer has the phone number

[45:15 - 45:30] everything is saved there, so now at least they have to know that they have to hide the sensitive information, for example, I hide the traders or the employees, they only see a part of the information, the rest of the phone number, the number of information in the account

[45:30 - 45:45] That's the first thing, the second thing is to apply one more thing, what is it called? Normally, there is a trick, normally I think that my data file on the operating network is not readable That's what we think, we think that our data file is binary

[45:45 - 46:00] And we need to have a command to query it. But in fact, in that hexa part, it has its own rules, it has its own structure. So if any father can build a data file, it will still be able to extract our data.

[46:00 - 46:15] So there are some parties that will do one more thing How do you code that physical file? However, there is a very important thing The database will need a key to read that file If the father loses the key, he will sacrifice

[46:15 - 46:30] I would like to share with you about the PCI DSS standard applied to database. It is being applied in Vietnam. There are two ways to use database. In the next part, I will share the so-called tokenization technology in the networkization of sensitive information.

[46:30 - 46:45] The tokenization will replace the number of the card, the PAN, into a token, a meaning chain. This token will be used to pay, pay, capture, refund, instead of we have to fill in the form.

[46:45 - 47:00] in the request. The goal is to reduce the scope of our research into these data. For tokenization, when designing, we need to consider the requirements

[47:00 - 47:15] related to the life cycle of a light cycle token, it will be used in a transaction and keep the information related to Merchant to ensure that the errors are avoided related to the core Merchant. Then it relates to security, we can use

[47:15 - 47:30] phần cứng hoặc là một cái service để mạng hóa như anh Huy có chia sẻ là cái khi mà mình muốn mạng hóa cả database thì thường mình sẽ có một cái thiết bị phần cứng

[47:30 - 47:45] and I will save that device and save the key to code all of the database's data files However, on a simpler level, that is, I just want to save some fields in the database to code

[47:45 - 48:00] It will help us, for example, a deaf person can't know what the actual data is like The data of the card is extremely dangerous Therefore, we will need

[48:00 - 48:15] to have a code system and decoding as well as these keys it will need to rotate that is to say it needs to change regularly and finally that is to say all the tree sorts related to tokens will have to be locked so then

[48:15 - 48:30] So what is its use case? When a user loads information related to a specific information, it will usually be loaded into our iframe and we will call the API

[48:30 - 48:45] The token line returns the respawn as a token as well as the information that it is just enough It doesn't have too much information And then this token will be used to make it look like a

[48:45 - 49:00] a number to do the payment through the payment port. In this section, I will talk more clearly about how we can code and decode this data through

[49:00 - 49:15] called Key Management Service of AWS. As you can see, this is Merchant. This is our gateway. This is AWS service. And this is where we will keep

[49:15 - 49:30] If the data is already encrypted, it will usually be stored in the database. The first stage is when we tokenization, that is, we want to encrypt the data, we will request a data key.

[49:30 - 49:45] This service will give us a data key This data key we will use to encrypt the data And then we will store the data that has been encrypted into the database The next step is when we want to pay

[49:45 - 50:00] In contrast, we will take the information from the database to decode. When the information has been decoded, we can use it to continue

[50:00 - 50:15] In the task of payment of credit card, there are two very important concepts, which are Settlement and Reconciliation.

[50:15 - 50:30] This is one of the factors that we need to be extremely important to capture whether the money is really transferred successfully or not. In the transaction processing system,

[50:30 - 50:45] After the transaction has been authorized and captured, the money has not yet been transferred to Merchant's account. And Ngoc will have to go through two stages, which are settlement, that is, carrying out the transaction.

[50:45 - 51:00] money transfer between banks, banks and merchants. And finally, that is the reconciliation. That is, the data exchange between the parties. This part is usually implemented by the payment gateway.

[51:00 - 51:15] It will have to connect the data between the bank and the transaction data in the database to ensure that the transactions from the customer pass through our webhook and we record them in the database.

[51:15 - 51:30] In order to design a data analysis system like this, we need to find out what the source data is.

[51:30 - 51:45] correct card they handle payment they have they usually have settlement system when the system is handled everyday they will generate report daily and our mission is to be able

[51:45 - 52:00] we can download or we can pull through SFTP. So what is our solution? We will have a schedule job here. We will download this file every day. And usually this file will be CSV or XML.

[52:00 - 52:15] At the same time, we will read the transaction data in the database related to the transaction in the day. We will compare to see if this transaction is related to each other.

[52:15 - 52:30] And finally, in order for the status to be best controlled in the database, we can send an update status request to the transaction processor

[52:30 - 52:45] update to the last status. So, we have successfully rescheduled this transaction. There will be no need to change anything else. So, when we design a system related to credit card payment system,

[52:45 - 53:00] In this process, we need to consider the components of the logic in the system. First of all, we have the components of the logic.

[53:00 - 53:15] client layer where customers and merchants will send payment requests to the system. The second is the object related to the third party, where it is actually processing the

[53:15 - 53:30] and the payment gateway that we are building. When we receive a request from the client, we will always

[53:30 - 53:45] before putting it in the payment processor. In this design, I will talk about how I will divide into objects inside the system so that everyone can understand the value.

[53:45 - 54:00] This payment processor is like the heart of the system when handling this transaction. It will be responsible for communicating so that we can tokenize and encode the data. Then it will decide whether or not the transaction is successful.

[54:00 - 54:15] which merchants want to enable or perform this 3DS. This is the configuration part. As for the actual display of the 3DS form, it will be on the side of the customer's card issuer bank.

[54:15 - 54:30] it will open an iframe here and the customer will fill in the OTP and in this part, it will mention that I will construct the enable and disable

[54:30 - 54:45] related to lock and so on. In the loop when we deal with transactions, these transactions must be logged and monitored.

[54:45 - 55:00] And when the system's tasks become more complicated, the payment processor will have to deal with the issue of asset-challenged processing.

[55:00 - 55:15] When there is a request to handle the tasks, I will prioritize the design and put it in MagicQ to ensure the ability to save data as well as handle all the requests.

[55:15 - 55:30] And finally, one of the indispensable components in this field is the database, the search. In this case, what you usually see is the search results.

[55:30 - 55:45] data about history, for example, history in these people is usually the history of a month, the rate of update and change is very low, right? The status update data is very low, so we completely have to separate the history data separately into one place and the online data

[55:45 - 56:00] In a separate place So, our online data will be almost always very uniform It's just a small part And if we put the whole history of online in one piece That is, we do not have a data lifecycle Then the life of this database will also become a very large place

[56:00 - 56:15] If we are lucky enough to have many customers, it will be terrible. All of you, if you make an online payment gateway system, you will have to remember a concept that is very important.

[56:15 - 56:30] It's called data life, just like in the past when I caught this idea, I used to work with Banking Bank. I used to work with Ocean Bank Banking Bank at the beginning of my life. Then he saw that, ah, the design guy, he put it down to the fact that the daily trading tables,

[56:30 - 56:45] It is divided into the daily and the history table The daily data is only stored in the daily table Then at the end of the day It runs a job called end of day EOD, any bank runs like that It calculates, it checks the data, the day it closes, it closes the notebook Then it will store the data

[56:45 - 57:00] Every day, after it is put into the history table, after it is put into the history table, it erases the day table. So that the next day, the day table is a little better and it runs very smoothly, it is very smooth, the performance is always stable.

[57:00 - 57:15] its design is LD or some T24 banks it is called CLOB its thinking is the same, just called different names LD is end of day, CLOB is close of business

[57:15 - 57:30] So now we can see a picture of the overall architecture Now add some components after you have

[57:30 - 57:45] There are men who are related to the credit card, right? Then add some more ingredients At that time, I looked at it, it was ok It was clearer than anything else For this concrete architecture You can see that Compared to the old architecture It will expand

[57:45 - 58:00] The first thing is that it will expand on the part of the suitable object in the system. We have another payment method, which is credit card. The next object that we expand here is related to the level of our business.

[58:00 - 58:15] of the system, we have more monitoring, audit log, we have more tasks related to settlement, reconciliation. And we will have one more layer related to data layer, we need to store

[58:15 - 58:30] of token volume data. This will also reflect the design mindset and the system's expansion. That is, if later when we expand the system's ports,

[58:30 - 58:45] If we want to integrate external payment systems and partners, or if we want to deploy an electronic device, we have to think first about where we will integrate it in this architecture.

[58:45 - 59:00] Then we shared for a while, then you will see that the performance is according to my experience So why do I share a lot about the part I always ask you is what is the weakness And usually you will see that the weakness is the dataway And this is my point of view

[59:00 - 59:15] If you guys want to use your career to become rich, sooner or later, you will also invest in the last resort. I'm not saying the last resort is for you guys. I mean sooner or later, you will also invest in the last resort. That's it.

[59:15 - 59:30] The more it grows, the slower it will slow down. And the important thing is that our customers pay a lot of money. It's easy for the company to pay a lot of money or our managers to accept that it is important and handle it. And in terms of experience, if it is expanded,

[59:30 - 59:45] If you look at this system, up to 80-90% will be related to the knowledge of your computer. Then you will do enough, you will see. This is the thing that I only saw 10 years ago. And 10 years later, it's still right.

[59:45 - 60:00] This is the reason why I set the door, about 10 years ago, I set the door to Udata Play. You will see that if you guys do a system now, let's say I make a system called Payment Gateway. Unfortunately, I don't have customers now. But if there are more customers,

[60:00 - 60:15] I will need a dev or someone to design the SA for me that gives me the ability to design the database for it For example, I told you to choose a database for your phone According to you, what database do you choose for this DB? There are people who say Oracle

[60:15 - 60:30] Some of you said Post-Sweat, some of you will have a different angle, right? Some of you said RMS, OK, OK, there are a lot of different angles. So when we choose database, even when we choose database,

[60:30 - 60:45] know first what is different from Database. Of course, besides the license, you will say that the money is temporarily taxed, we are not related to money. Ok, you see, it will be different in architecture, it will be different in Database engine. What does that mean? If you see

[60:45 - 61:00] There are two people You choose Two people Choose between 18 years old Or 19 years old 18, 19, 20 Or 25 years old It doesn't matter Because the first thing They think is When they encounter Their problems Then the database is the same Each database It is

[61:00 - 61:15] and they can learn a different kind of skill For example, the one who is good at drawing, the one who is good at math, the one who is good at physics, the one who is good at biology So you guys have to know how to choose the right person for your course Do you understand? How to handle yourself For example, there are a lot of DML systems You have to understand that

[61:15 - 61:30] For example, if we use PostgreSQL, then the behavior of PostgreSQL is completely different from Oracle and SQL Server Because the architecture of PostgreSQL is MVCC, so the method will be very different from Oracle That is, when we choose, we have to know the principle, it is extremely different

[61:30 - 61:45] And when you really only have one thing, you have the power of love. That is, you have something at a distance. If you look at it from a distance, you have the power of love, then you will be very different. So I have a next question.

[61:45 - 62:00] How can you be in love with different types of nanotubbies? For example, if you have a red bean, you can use Postgres to be in love with it, right? If you have a red bean and it uses Postgres, how can you be in love with it?

[62:00 - 62:15] But if we go to another side, they use Oracle, we still have to love And if we go to another side, they use SQL Server, we still have to play Or if they don't use Payment Gateway, in this article we share about Payment Gateway But if we go to e-commerce system, they will say

[62:15 - 62:30] Now I don't know what to do with e-commerce. Or go to the hospital system, I love the hospital system. If you don't go to the hospital, you won't get used to the service, you won't be able to play. Then we are very difficult to become a robot. I have done my research.

[62:30 - 62:45] My school is Tối Ưu. You can sign up for one-on-one consultations with me. I will show you how to break through in Tối Ưu extremely quickly and how you can create a lot of opportunities in your career. I have shared very carefully that

[62:45 - 63:00] When we have a different path That is, you look at it from a more distant point of view Hit the places that are really Sooner or later, the system will need it Then you will eat Sooner or later, the system will need it Even if it's small now When you grow up, sooner or later, it will need it

[63:00 - 63:00] Come on.



---
*Generated using Whisper large v3 and processed automatically*
