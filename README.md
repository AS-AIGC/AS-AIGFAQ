# AS-AIGFAQ

## The current norm and issues of administrative services

- All laws, service explanations, and announcements will be posted on the website.
- The website is like a big maze where everything is available, but what you're looking for is often hard to find.
- The quickest way is to call the responsible person and ask, but this leads to them spending a lot of time answering similar questions, ultimately reducing their availability to handle daily public affairs.

## Existing Solutions for Administrative Services

- Single Service Window: Staffed by professional customer service representatives who can answer simple questions. However, complex questions still need to be referred to caseworkers, the response time for referral cases is prolonged, and the customer service representative may make errors in judgment.
- Organizing FAQ for users to self-check: A dedicated team writes and updates the FAQ regularly. However, the wording, tone, and type of questions in the FAQ are difficult to standardize, and updating it can be prone to oversight.
- Introducing a chatbot: A conversational bot designed based on a database to answer questions. However, it can only answer standardized questions and requires a significant cost for fine-tuning.

## Our Solution

- Let ChatGPT provide suggestions for questions that users may be interested in, thereby achieving the goal of automatically generating FAQs.
- Use the OpenAI API to cast a spell (prompt) that prompts ChatGPT to ask questions based on the input content (context, i.e. relevant regulations); then ask ChatGPT to answer the collected questions based on the input content.
- Google colab notebook： [[colab_notebook_AS_FAQ.ipynb](colab_notebook_AS_FAQ.ipynb)] [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AS-AIGFAQ/AS-AIGFAQ/blob/main/colab_notebook_AS_AIGFAQ.ipynb)

## Case Sharing

- FAQ for Academic Grant Applications at Academia Sinica
  - Original data CSV file: [[AS-proposal.csv](examples/AS-proposal.csv)]
  - Generated FAQ file: [[AS-proposal-QA.csv](examples/AS-proposal-QA.csv)]
  - Generated HTML file: [[AS-proposal-QA.csv.html](examples/AS-proposal-QA.csv.html)]
  - Demo：https://aws.cclljj.net/AS-FAQ/proposal.html
- FAQ for Information Services at Academia Sinica
  - Original data CSV file: [[AS-ITS.csv](examples/AS-ITS.csv)]
  - Generated FAQ file: [[AS-ITS-QA.csv](examples/AS-ITS-QA.csv)]
  - Generated HTML file: [[AS-ITS-QA.csv.html](examples/AS-ITS-QA.csv.html)]
  - Demo：https://aws.cclljj.net/AS-FAQ/ITS.html 

  
## Development Team

- Department of Information Technology Services, Academia Sinica
- Institute of Information Science, Academia Sinica

---

---


## 現有行政服務的常態與問題

- 所有的法條、服務說明、公告事項都會放置在網站上
- 網頁就像一個大迷宮，什麼都有，但是想找的往往都找不到
- 最快的方法就是打電話問承辦人，導致承辦人花費大量的時間在回答類似的問題，反而減少可以處理日常公務的時間

## 現有行政服務的解方

- 單一服務窗口：由專業客服代為回答簡易問題。但是，複雜問題仍須轉介承辦人、轉介案的回應所需時間拉長、客服可能判斷錯誤
- 整理 FAQ 讓使用者自行查詢：由專人撰寫且隨時更新 FAQ。但是，FAQ 的文句、口氣、題目類型難以標準化；更新時容易掛一漏萬
- 導入 chatbot ：根據資料庫設計交談式機器人回答問題。但是，往往只能回答制式問題、需花費大量成本進行調校

## 我們的解法

- 讓 ChatGPT 提供對使用者感興趣的問題建議，進而達到自動生成 FAQ 的目標
- 透過 OpenAI API，施展咒語 (prompt) 讓 ChatGPT 依據輸入的內容 (context，即相關規定) 提出問題；接著再請 ChatGPT 依據輸入的內容，回答所收集到的問題
- Google colab notebook： [[colab_notebook_AS_FAQ.ipynb](colab_notebook_AS_FAQ.ipynb)] [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AS-AIGFAQ/AS-AIGFAQ/blob/main/colab_notebook_AS_AIGFAQ.ipynb)

## 案例分享

- 中央研究院學術計畫申請 FAQ
  - 原始資料 CSV 檔：[[AS-proposal.csv](examples/AS-proposal.csv)]
  - 產製 FAQ 檔：[[AS-proposal-QA.csv](examples/AS-proposal-QA.csv)]
  - 產製 HTML 檔：[[AS-proposal-QA.csv.html](examples/AS-proposal-QA.csv.html)]
  - Demo：https://aws.cclljj.net/AS-FAQ/proposal.html
- 中央研究院資訊服務 FAQ
  - 原始資料 CSV 檔：[[AS-ITS.csv](examples/AS-ITS.csv)]
  - 產製 FAQ 檔：[[AS-ITS-QA.csv](examples/AS-ITS-QA.csv)]
  - 產製 HTML 檔：[[AS-ITS-QA.csv.html](examples/AS-ITS-QA.csv.html)]
  - Demo：https://aws.cclljj.net/AS-FAQ/ITS.html 

  
## 開發團隊

- 中央研究院 資訊服務處
- 中央研究院 資訊科學研究所
