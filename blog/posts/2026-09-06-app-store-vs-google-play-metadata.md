---
title: App Store vs Google Play: how your metadata really works on each store
description: App Store vs Google Play compared field by field: title, subtitle, keywords, description, character limits, indexing rules and localization. What solo developers get wrong and how to write once for both stores.
date: 2026-09-06
tags: app store, google play, aso, metadata, indie
slug: app-store-vs-google-play-metadata
---

When I shipped my first app, I wrote one description in English, pasted it into App Store Connect and into the Play Console, and assumed I was done. Two stores, same app, same text. What could go wrong?

Everything. A month later the app was indexed for almost nothing on Google Play, and on iOS I was wasting half my keyword space without knowing it. The two stores look similar from the outside, but they read your metadata in completely different ways. Here is the comparison I wish I had read before launching.

## The 30 characters both stores give you

Both the App Store and Google Play cap the app title at 30 characters. That is where the similarities end.

On iOS, the title is the strongest ranking field you control. Keywords in the title carry more weight than anywhere else, so a title like "RunTrack: GPS Run Tracker" beats "RunTrack" for discovery.

On Google Play, the title also matters a lot, but Google applies stricter policy rules: no keyword stuffing, no superlatives like "best" or "#1" used purely for promotion, no store ranking claims. Developers have had apps rejected for titles that would be fine on iOS. The safe play on Android is a brand name plus one clear functional keyword, not three.

## The subtitle trap

iOS gives you a 30-character subtitle, shown under the title in search results and indexed for keywords. It is a second title in disguise, and most indie developers waste it on marketing fluff like "your companion for life".

Google Play has no subtitle field at all. The rough equivalent is the short description, 80 characters maximum, shown on your listing page. It works differently: Google reads it as the start of your app description, and it heavily influences conversion because it is often the only text a user reads before deciding. On iOS your subtitle ranks you. On Android your short description convinces people who already found you.

## Where keyword targeting actually happens

This is the biggest structural difference.

iOS has a hidden keywords field: 100 characters, comma separated, invisible to users but fully indexed by Apple. This is where long-tail keyword research pays off. You do not need to repeat words already in your title or subtitle (Apple combines them automatically), do not use plural forms if you have the singular, and do not waste characters on spaces after commas.

Google Play has no keywords field. None. Google indexes your app from your title, short description and full description, the same way it indexes web pages. That is why repeating your main keywords naturally a few times inside the full description matters on Android, while the same repetition on iOS does nothing because the description is barely indexed.

## The description: read on Android, ignored on iOS

This one cost me real traffic.

The App Store indexes the title, subtitle and keywords field. The promotional text and the long description have almost no effect on search ranking. The description is a conversion tool: it convinces people who already landed on your page. Write it for humans, front-load the first two lines (everything after that hides behind "more"), and do not expect any SEO benefit.

Google Play reads the full description and uses it for ranking. Keyword research that looks optional on iOS is mandatory on Android. The practical rule many ASO specialists use: your main keyword should appear in the title, once in the short description, and a few times, naturally, inside the 4,000-character description. Stuffing it twenty times gets you flagged; mentioning it once gets you nowhere.

## Localization: the multiplier almost everyone skips

Here is where both stores agree, and where most indie apps throw away the easiest traffic available.

Both stores let you create fully localized listings: title, subtitle or short description, description, keywords on iOS, and localized screenshots. The vast majority of listings on both stores exist in English US only. Meanwhile, a large share of downloads worldwide comes from users searching in their own language, and some markets (Japan, Korea, Germany, Brazil) convert at high rates with far less keyword competition than English.

Only ranking for English US means you are invisible for most of the planet's searches. And think about your niche geographically: a football stats app has no reason to fight for positions in countries where football is a minor sport, when Spain, Brazil or Indonesia would convert far better per impression. Localized metadata is how you claim those searches without paying a cent for ads.

The catch is volume. Localizing a full listing properly into 10 or 20 languages by hand means rewriting the title, subtitle, description, keyword set and screenshots for every language. Nobody does this consistently with a spreadsheet. It is exactly the kind of repetitive, mechanical work that kills indie projects.

## What this means in practice, field by field

Title (30 chars): brand plus one keyword on iOS, brand plus one safe keyword on Android.

Subtitle (iOS only, 30 chars): one more keyword phrase, not a slogan.

Keywords (iOS only, 100 chars): your long-tail strategy, no repeats, no spaces after commas.

Short description (Android only, 80 chars): your main keyword plus a conversion hook.

Full description: conversion copy on iOS, ranking text on Android.

Localization: the single highest-leverage move on both stores, and the one nobody has time to do by hand.

## Verdict

Stop treating the two stores as one. Write your iOS metadata with the subtitle and keywords field as the ranking core and the description as pure sales copy. Write your Android metadata with the description as a real ranking document. Then localize both, because an unlocalized listing leaves most of the world's searches to your competitors.

Doing all of this by hand for every language is why people either skip localization or burn a weekend per language. It is also why I built AsoFast: it generates the title, subtitle, description and keyword set for each store with AI, translates everything into 80+ languages, and publishes straight to App Store Connect and the Play Console. It runs 100% locally on your machine, your store credentials never leave your computer, it is open source under the MIT license, and it is free. If you are tired of paying AppTweak $79 a month or ASODesk $29.99 just to write metadata, grab it here: https://github.com/ediaStudio/asofast
