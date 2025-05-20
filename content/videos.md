+++
title = 'Videos'
date = 2024-08-13T23:03:12-04:00
draft = false
+++
<!-- markdownlint-disable MD025 MD033 MD045 MD013 -->

<style>
  .video-showcase {
    margin: 0 auto;
    max-width: 1200px;
  }
  
  .video-container {
    margin-bottom: 60px;
    border-radius: 12px;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(40,40,40,0.9) 0%, rgba(20,20,20,0.9) 100%);
    box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .video-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
  }
  
  .video-header {
    padding: 20px 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(90deg, rgba(60,60,60,0.8) 0%, rgba(30,30,30,0.8) 100%);
    border-bottom: 1px solid rgba(255,255,255,0.1);
  }
  
  .video-title {
    margin: 0;
    color: #fff;
    font-size: 1.5em;
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
  }
  
  .video-date {
    background-color: rgba(255,255,255,0.1);
    color: #fff;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 500;
    letter-spacing: 1px;
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
    font-size: 1.1em;
    line-height: 1.6;
  }
  
  @media (max-width: 768px) {
    .video-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 10px;
    }
    
    .video-title {
      font-size: 1.3em;
    }
  }
</style>

<div class="video-showcase">
  <div class="video-container">
    <div class="video-header">
      <h2 class="video-title">Biederman's Deli</h2>
      <span class="video-date">February 7, 2025</span>
    </div>
    <div class="video-embed">
      {{< youtubepl id=PLxS9axl1j35v_RoQtCo30D3fRU4djCffT title="Crawlspace - Biederman's Deli - 2025/02/07" >}}
    </div>
    <div class="video-description">
      Crawlspace live at Biederman's Deli in Nashua, NH. The band delivered a high-energy set featuring improvisational jams and fan favorites.
    </div>
  </div>
  
  <div class="video-container">
    <div class="video-header">
      <h2 class="video-title">Biederman's Deli</h2>
      <span class="video-date">January 10, 2025</span>
    </div>
    <div class="video-embed">
      {{< youtubepl id=PLxS9axl1j35ubPr4sb3p37KMq8ZZSbA_J title="Crawlspace - Biederman's Deli - 2025/01/10" >}}
    </div>
    <div class="video-description">
      The band's first show of 2025 at Biederman's Deli packed the house for a night of original music and extended improvisations.
    </div>
  </div>
  
  <div class="video-container">
    <div class="video-header">
      <h2 class="video-title">BNH Stage</h2>
      <span class="video-date">July 20, 2024</span>
    </div>
    <div class="video-embed">
      {{< youtubepl id=PLxS9axl1j35tF_RNGhADtkk5VlydS2gFN title="Crawlspace - BNH Stage - 2024/07/20" >}}
    </div>
    <div class="video-description">
      Crawlspace performing outdoors at the BNH Stage during the height of summer. This show featured guest appearances and new material.
    </div>
  </div>
</div>