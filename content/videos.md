+++
title = 'Videos'
description = 'Watch Crawlspace live performances from venues across New Hampshire including Biederman\'s Deli and BNH Stage'
date = 2024-08-13T23:03:12-04:00
lastmod = 2025-10-19T14:35:00-04:00
draft = false
+++
<!-- markdownlint-disable MD025 MD033 MD045 MD013 -->

<style>
  .video-showcase {
    margin: 0 auto;
    max-width: 1200px;
    font-family: "Lora", serif;
    font-size: 21px;
    line-height: 33px;
    letter-spacing: -0.2px;
    color: #848d96;
  }

  .video-container {
    margin-bottom: 60px;
    border-radius: 12px;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(40,40,40,0.9) 0%, rgba(20,20,20,0.9) 100%);
    box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    width: 95%;
    max-width: 95%;
    margin-left: auto;
    margin-right: auto;
  }

  .video-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
  }

  .video-header {
    padding: 20px 30px;
    background: linear-gradient(90deg, rgba(60,60,60,0.8) 0%, rgba(30,30,30,0.8) 100%);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    color: #47bec7;
  }

  .video-title-with-date {
    margin: 0;
    padding: 0;
    font-family: "Montserrat", sans-serif;
    font-weight: 600;
    font-size: 0.85em;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    line-height: 1.2;
    display: block;
  }

  h2.video-title-with-date {
    margin: 0;
    padding: 0;
    margin-block-start: 0;
    margin-block-end: 0;
    line-height: 1;
  }

  .video-date-inline {
    font-size: 0.75em;
    color: #848d96;
    font-weight: 400;
    opacity: 0.8;
  }

  .video-embed {
    position: relative;
    padding-bottom: 56.25%;
    height: 0;
    overflow: hidden;
  }

  .video-embed iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: 0;
  }

  .video-description {
    padding: 20px 30px;
    color: rgba(255,255,255,0.8);
    font-family: "Lora", serif;
    font-size: 15.75px; /* Reduced by 25% from 21px */
    line-height: 24.75px; /* Reduced by 25% from 33px to maintain proportion */
    letter-spacing: -0.2px;
  }

  @media (max-width: 768px) {
    .video-title-with-date {
      font-size: 0.8em;
    }
  }
</style>

<div class="video-showcase">
  <div class="video-container">
    <div class="video-header">
      <h2 class="video-title-with-date">Biederman's Deli <span class="video-date-inline"><br>07/02/2025</span></h2>
    </div>
    <div class="video-embed">
      {{< youtubepl id=PLxS9axl1j35v_RoQtCo30D3fRU4djCffT title="Crawlspace - Biederman's Deli - 2025/02/07" >}}
    </div>
    <div class="video-description">
      Crawlspace live at Biederman's Deli in Plymouth, NH. The band delivered a high-energy set featuring improvisational jams and fan favorites.
    </div>
  </div>

  <div class="video-container">
    <div class="video-header">
      <h2 class="video-title-with-date">Biederman's Deli <span class="video-date-inline"><br>10/01/2025</span></h2>
    </div>
    <div class="video-embed">
      {{< youtubepl id=PLxS9axl1j35ubPr4sb3p37KMq8ZZSbA_J title="Crawlspace - Biederman's Deli - 2025/01/10" >}}
    </div>
    <div class="video-description">
      The band's first show of 2025 at Biederman's Deli packed the house for a night of great songs and extended improvisations.
    </div>
  </div>

  <div class="video-container">
    <div class="video-header">
      <h2 class="video-title-with-date">BNH Stage <span class="video-date-inline"><br>20/07/2024</span></h2>
    </div>
    <div class="video-embed">
      {{< youtubepl id=PLxS9axl1j35tF_RNGhADtkk5VlydS2gFN title="Crawlspace - BNH Stage - 2024/07/20" >}}
    </div>
    <div class="video-description">
      Crawlspace performing at the BNH Stage in Concord, NH during the height of summer.
    </div>
  </div>
</div>
