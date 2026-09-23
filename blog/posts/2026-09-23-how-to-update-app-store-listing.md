---
title: How to update your app store listing after launch
description: What you can change on Google Play and the App Store once your app is live, which fields to fix first, and how to refresh your listing without erasing the traffic you already have.
date: 2026-09-23
tags: app store, google play, metadata, localization, aso
slug: how-to-update-app-store-listing
---

You shipped, and the listing you wrote in one evening now has to carry the next two years. Sooner or later you will want to change it: new keywords, new screenshots, a language you skipped. Updating a live listing is not the same job as writing the first one. You are editing something that already ranks, and each store handles updates differently.

**1. Know what each store lets you change without shipping a build.** On Google Play, the title, short description, full description, screenshots and graphics are edited straight from the store listing page, and review takes hours, not days. On the App Store, the name, subtitle, keywords, description and screenshots travel with a version, so they change when you submit an update. Plan the App Store refresh around your next release; on Play you can act today.

**2. Change one family of fields at a time.** A keyword swap, a screenshot rewrite and a title change are three separate experiments. Ship one, write down the date, then wait. Text takes a few days to reindex, and the effect on impressions needs a couple of weeks to show. Change everything at once and you learn nothing.

**3. Start with the fields that carry the ranking.** On the App Store, the title (30 characters), the subtitle (30) and the 100 character keyword field do the search work. The description mostly converts; it is not indexed. On Google Play there is no keyword field, so the title (30), the short description (80) and the full description (4000) are the only indexed text you have. Rewriting only your iOS description changes almost nothing in search. Spend the effort where the algorithm reads.

**4. Fix the keywords you already almost rank for.** Both consoles show the search terms that bring impressions and the countries they come from. The list is thin at first, and every line of it is real. A term where you sit at position 12 with a few impressions is a near miss one metadata change can move. A term you have never appeared for is a much longer fight. Rewrite toward the near misses, not the fantasy.

**5. If you only change one thing, add a language.** This is the update with the biggest upside for a solo developer, because most listings on both stores are English US only and the demand elsewhere is unclaimed. Searches differ by market, so translating your English keywords is not localizing them: you want the terms people actually type in that language. And your niche decides the market. A football app gains more from Brazil, Turkey or Indonesia than from one more English keyword, because the searches happen where the sport lives. Some languages bring downloads, others bring revenue. Check the countries in your console data, then cover the languages they read.

**6. Prepare the whole set before you touch the console.** Draft the new title, subtitle or short description, description, keywords and screenshots for every language first, and keep the current version so you can roll back. Check each field against its character limit before pasting: an App Store title overflow only shows up when you try to save. Doing this by hand across five languages is a full evening of copy, paste and counting.

**7. Verify after publishing.** Open both store pages and read every field. On Play the change appears within hours; on the App Store it lands with the version you submitted. Then search your main keyword on a phone and note your position. That number is the baseline for the next update.

A listing is never finished, it is maintained. The part that stopped me for months was translation: five languages, correct keywords per market, four character limits, one evening gone. That is the part I automated with [AsoFast](https://github.com/ediaStudio/asofast). It generates your title, subtitle, description and keywords for both stores, translates the listing into more than 80 languages, builds screenshot templates and publishes straight to App Store Connect and Google Play. Everything runs locally, your credentials stay on your machine, and it is free and open source under MIT. If ads are eating your budget, an updated listing is the cheapest experiment you can run this week.
