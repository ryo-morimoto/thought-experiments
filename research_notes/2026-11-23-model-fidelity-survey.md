# 手書きのモデルの忠実さを確かめる方法の先行研究（2026-11-23）

ユーザーの指摘（優先順位を会話の中のものだけから選んでいた）を受けて、経緯を知らない subagent 2 体に先行研究を調べさせた。1 体はブラウザ・Web の形式モデル、1 体は分野を問わない一般の方法。どちらにも、こちらの仮説（havoc、自己合成）は渡していない。以下は報告の要約で、[読] は subagent が本文の該当節を読んだもの、[要] は要旨や検索の抜粋だけのもの。筆者は論文を開いていない。抜き出した本文と覚え書きは、ジョブの一時ディレクトリの survey-web/ と survey-general/ に置いた（リポジトリには入れない）。

## 向きの区別

モデルでの安全性の証明が対象に移るのは、実装のすべての振る舞いがモデルの振る舞いであるとき（実装 ⊆ モデル、モデルが過近似）。モデルで見つけた反例が対象に移るのは逆の向き（モデル ⊆ 実装）。報告によれば、公表された「検証」の多くは片方の向きしか見ていない。

## ブラウザ・Web の形式モデル

- Akhawe ら、CSF 2010（Alloy、手書き）[読] https://css.csail.mit.edu/6.566/2018/readings/formal-web.pdf : 公理化は不完全と自ら述べる。見つけた攻撃の 1 つを実際の配備で確かめた。
- Featherweight Firefox（Bohannon と Pierce、WebApps 2010）[読] https://www.usenix.org/legacy/event/webapps10/tech/full_papers/Bohannon.pdf : 不明な所は HTML5 とブラウザの試行で決めた。意図して Firefox に合わせた所がある。体系的な検証は無い。
- Quark（Jang、Tatlock、Lerner、USENIX Security 2012）[読] https://www.usenix.org/system/files/conference/usenixsecurity12/sec12-final217.pdf : 向きを逆にし、ブラウザの核をモデルに合わせて作る。代わりに方策が標準から外れる。
- Web Infrastructure Model（Fett、Küsters、Schmitz、S&P 2014）[読] https://arxiv.org/abs/1403.1866 : 標準に沿って手で作り、実装とも照らしたと書くが、方法は書かない。見つけた攻撃を実際の BrowserID で確かめた。
- WebSpec（Veronese ら、S&P 2023）[一部読] https://arxiv.org/abs/2201.01649 : Coq のモデルの反例を WPT の試験に変えて Chrome と Firefox で動かす。著者は「正しさの証明ではなく経験的な証拠」と書く。深さや配列の大きさに上限がある。
- 履歴の移動（Brewster と Jeffrey、arXiv 2016）[読] https://arxiv.org/abs/1608.05444 : 仕様に沿ったモデルで性質が崩れ、反例を 5 つのブラウザで手で再生した。ブラウザどうしも食い違った。
- Cookie Crumbles（Squarcina ら、USENIX Security 2023）[読] https://www.usenix.org/conference/usenixsecurity23/presentation/squarcina : モデルは無く、試験の束を 3 エンジンで動かし、食い違いを標準と手で照らした。
- JS の類例: JSCert（POPL 2014）[読] https://www.doc.ic.ac.uk/~mbodin/esplorado/popl14.pdf 、KJS（PLDI 2015）[要]、JISET（ASE 2020、ECMA-262 の散文から機械的に取り出す）[読] https://plrg.korea.ac.kr/assets/data/publication/ase20-park-jiset.pdf 、JEST（ICSE 2021、エンジンと取り出した仕様の差分試験）[一部読] https://arxiv.org/abs/2102.07498 。
- 見つからなかったもの: WHATWG の HTML・Fetch の散文から機械的にモデルを取り出した研究。

報告者の推論（論文が明言してはいない）: ブラウザと照らすどの研究も、モデルが見つけた攻撃だけを確かめていて、「不変条件が成り立つ」という結果をブラウザで確かめたものは無い。

## 分野を問わない方法

- 実装の観測をモデルが許すかで確かめる（litmus と herd、Alglave ら、TOPLAS 2014）[要] https://arxiv.org/abs/1308.6810 : ハードウェアで観測した結果はすべてモデルが許さねばならない。実装 ⊆ モデルの向きの、通常行われる唯一の証拠。試した範囲だけ。
- トレースの検証（Cirstea ら 2024 [要] https://arxiv.org/abs/2404.16075 、Howard ら NSDI 2025 [要] https://arxiv.org/abs/2406.17455 ）: 実装のトレースを TLC で確かめる。実装の状態とモデルの変数の対応づけが費用の中心で、抽象的な仕様では難しかった（Davis ら PVLDB 2020 [要] https://arxiv.org/abs/2006.00915 ）。
- 実行できるモデルで適合試験を動かし、モデルの網羅を測る（Sail、POPL 2019 [7 節を読] https://www.cl.cam.ac.uk/~pes20/sail/sail-popl2019.pdf ）: 試験の作者の読みとの一致で、出荷中の実装との一致ではない。
- モデルから試験を作って実装で動かす（WebSpec、ioco）: 反例の向きで、証明の向きではない。
- 信頼の基盤の差分試験（Csmith、PLDI 2011 [読] ）: CompCert の手書きの意味の欠落（即値の幅の制約）を見つけた。証明では見つからない種類。
- モデルの中の検査（Reid OOPSLA 2017 [要]、空虚さの検出、網羅の尺度）: 衛生には要るが、忠実さの証拠ではない。変異でモデルの忠実さを測る確立した尺度は見つからなかった。
- 写していない部分を任意の値にする（havoc）: 1 つの実行の安全性には健全。詳細化は hyperproperty を保たない（Clarkson と Schneider、JCS 2010 [要]）。「健全な havoc」を主題にした論文は確かめられなかった。

## このリポジトリの作業との照合（筆者の推論）

- これまでの WPT との照合は、モデルを試験の作者の期待値と比べたもの（Sail の型）。直る前のブラウザでの再現試験と引き金の探索は、モデルからブラウザへの向き（WebSpec の型）。
- 実装 ⊆ モデルの向き（ブラウザが実際に返した値を、モデルが許すか）は、まだやっていない。wpt-cases.tsv の各エンジンの結果は合否だけで、失敗したときの実際の値は持っていない。
