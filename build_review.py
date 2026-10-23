import json,csv,zipfile,os
root='/mnt/data/fund-answer-reviewed'; p=f'{root}/questions.json'; d=json.load(open(p,encoding='utf-8'))
confirmed={4:'金錢、有價證券與著作權均可作為信託財產，D符合題意。',20:'物價上漲降低實質購買力，屬通貨膨脹風險，C。',63:'證券經紀屬交易中介，非資產管理；A。',90:'債券、貨幣市場及特別股均可能偏向收益訴求，D。',100:'外幣相對新台幣貶值，外幣計價資產換回台幣減少；B敘述顛倒。D屬投資建議，不應視為無條件保證。',108:'β可用個別資產與市場報酬共變異數除以市場變異數計算，不必使用個別基金標準差，C。',109:'不同時段及市場條件下實際報酬不固定，D。',115:'300000/30=10000美元；10美元買入1000單位；贖回12000美元；按贖回金額衡量匯率影響=12000×(28.5−30)=−18000元，D。注意若按原始本金衡量會是−15000元，需說明口徑。',146:'境外基金可能同時有匯率、流動性與資訊風險，D。',149:'境外所得本身非健保補充保費列舉的扣費所得，D；具體配息性質仍需辨別。',174:'匯率、OPEC產量決策與景氣循環均會影響能源市場，D。',179:'100000×95%＋100000×30%×50%=110000，C。',194:'台灣50正2為正向槓桿曝險，不能用於規避股市下跌，D。'}
needs={25:'2021年多幣別私募基金投資海外最低比率：需查當時主管機關規定。',42:'境外基金總代理之基金成立年限屬法規條件，須查題目適用版本。',117:'基金募集申報生效制之例外與法規沿革需查教材版本。',131:'衍生商品風險暴露40%門檻需核對當期規範。',138:'A印製費用與B管理費、C保管費的負擔來源不同；題庫D「皆是」與常見費用分類有疑義，優先核對教材。',139:'2021年補充保費2.11%屬歷史費率，與現行規定應區分。',140:'2萬元門檻與扣費所得類型需核對適用規範。',142:'私募應募人99人上限需核對基金類型及法規版本。',147:'海外所得100萬元計入門檻須與基本所得額免稅額區分。',148:'750萬元為特定年度基本所得額門檻，須核對題目適用年度。',150:'2013年海外投資業務委外70%門檻，需核對當時公告。',155:'境外基金投資中國有價證券20%限制需核對法規版本。',193:'教材答案A與D「A、B、C皆是」並列；B、C的5筆門檻是否符合當時資格需查正式規定。'}
assert len(confirmed)+len(needs)==26
rows=[]
for q in d:
 i=q['id']
 if i in confirmed:
  q['answer_review']='概念或計算初步核實（非官方題解）';q['answer_review_note']=confirmed[i]
 elif i in needs:
  q['answer_review']='法規版本或教材答案待查證';q['answer_review_note']=needs[i]
 else:
  q['answer_review']='未獨立複核';q['answer_review_note']=''
 if i in confirmed or i in needs:
  rows.append([i,q['chapter'],q['text'],q['answer'],q['answer_review'],q['answer_review_note']])
with open(p,'w',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2)
with open(f'{root}/26題答案重點核對.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['題號','章節','題目','教材答案','本輪狀態','說明']);w.writerows(rows)
with open(f'{root}/ANSWER-REVIEW-26.md','w',encoding='utf-8') as f:
 f.write('# Sunny Fund Review｜26 題答案重點核對\n\n本輪對前次挑出的 26 題進行概念與算式初步檢查；**不是法規正式查證，也不是200題答案全部驗證**。教材答案均保留。\n\n')
 f.write('## 概念／算式初步核實（13 題）\n\n')
 for i,s in confirmed.items():f.write(f'- 第 {i} 題（教材答案 {d[i-1]["answer"]}）：{s}\n')
 f.write('\n## 仍需查法規版本／教材題解（13 題）\n\n')
 for i,s in needs.items():f.write(f'- 第 {i} 題（教材答案 {d[i-1]["answer"]}）：{s}\n')
 f.write('\n## 核對界線\n\n本輪的「初步核實」僅是題意、基本金融概念或數學算式檢查，不等同教材出版者或主管機關確認。法規題未查證歷史版本前，請以教材作答並保留疑點。\n')
with open(f'{root}/README.md','a',encoding='utf-8') as f:f.write('\n\n### 最新答案重點核對\n詳見 `ANSWER-REVIEW-26.md` 與 `26題答案重點核對.csv`。26題中13題完成概念/算式初步核實，13題仍需法規或教材題解查證。其他174題尚未獨立複核答案。\n')
output='/mnt/data/sunny-fund-review-200-answer-review-26.zip'
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for dirpath,_,files in os.walk(root):
  for name in files:
   if name=='build_review.py':continue
   path=os.path.join(dirpath,name);z.write(path,os.path.relpath(path,root))
with zipfile.ZipFile(output) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.startswith('assets/q') and n.endswith('.webp')])==200
 assert len(json.loads(z.read('questions.json')))==200
print(output,os.path.getsize(output),'verified',len(confirmed),'pending',len(needs))
