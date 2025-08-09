#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包括的字幕翻訳システム
======================

Chapter 02 Basic Logic の字幕を包括的に翻訳
自然な日本語字幕として表示されるよう調整

使用方法:
    python comprehensive_subtitle_translator.py chapter_02_translation_queue.json
"""

import json
import os
import sys
from pathlib import Path

class ComprehensiveSubtitleTranslator:
    def __init__(self):
        # Chapter 02専用の包括的字幕翻訳辞書
        self.comprehensive_translations = {
            # Segment 1 (00:00:09 - 00:00:36)
            "So whenever I'm starting work on a new tool, I like to have some kind of placeholder geometry so that I can test my tool in the appropriate context. In this case, I made something that should kind of represent a landscape with maybe some environment assets on it. You know, imagine that this is gonna be like some big boulders that we wanna build our bridge across and you can just make that with a grid, add some noise from mountain nodes and you know, add some spheres, merge it together,.": 
            "新しいツールの作業を始める際は、適切なコンテキストでツールをテストできるよう、何らかのプレースホルダージオメトリを用意するようにしています。今回は、いくつかの環境アセットが配置されたランドスケープのようなものを作成しました。これは、橋を架けたい大きな岩石のようなものを想像してください。グリッドで作成し、Mountainノードでノイズを追加、スフィアを追加してマージするだけです。",
            
            # Segment 2 (00:00:36 - 00:01:04.5)
            "and then you have something like this. And to actually use the tool, the artist would then use lines inside Unreal that are supplied by Houdini engine to get a similar experience within Houdini. To test it, you can just get the curve node and make sure to set it to polygon mode and to draw on our little placeholder environment, we can press enter to get into the drawing mode and you can see it over here, the little curve tool overlay.":
            "すると、このような結果が得られます。実際にツールを使用する場合、アーティストはUnreal内でHoudini Engineが提供するラインを使用し、Houdini内で同様の体験を得ます。テストするには、Curveノードを取得してポリゴンモードに設定します。小さなプレースホルダー環境上で描画するには、Enterキーを押して描画モードに入ります。こちらに小さなカーブツールオーバーレイが表示されます。",
            
            # Segment 3 (00:01:04.5 - 00:01:22.5)
            "And I have also enabled primitive snapping that makes sure that whatever we're drawing is actually gonna, you know, end up where we want it and not be somewhere in the distance or something. Lemme just make a curve that makes sense. So I'm just gonna press enter and then you know, maybe draw a curve like this.":
            "プリミティブスナッピングも有効にしています。これにより、描画する内容が実際に望む場所に配置され、遠くの場所などに配置されることがありません。意味のあるカーブを作成しましょう。Enterキーを押して、このようなカーブを描画します。",
            
            # Segment 4 (00:01:24 - 00:01:42)
            "I can't see it right now because these two are not linked up together. But maybe I can just click the blue flag on my curve and then have the environment be in wire frame mode. And I'm also gonna enable something like the display points feature so that we can see the vertices of our curve.":
            "現在は2つが連結されていないため見えません。カーブの青いフラグをクリックして、環境をワイヤーフレームモードにします。また、ポイント表示機能も有効にして、カーブの頂点を確認できるようにします。",
            
            # Segment 5 (00:01:42 - 00:02:04.5)  
            "And yeah, and as you can see it's a pretty simple spline. It just, it's all it is is just these corner points and they're connected straight from one point to the next. But that's of course not what we want because as you saw in the preview, the final result should be kind of like free flowing, and should have some kind of minimum offset from the landscape or, or the assets in our environment.":
            "ご覧の通り、これは非常にシンプルなスプラインです。単に、これらのコーナーポイントがあるだけで、ポイントから次のポイントへ直線で接続されています。しかし、これは当然望む結果ではありません。プレビューで見たように、最終結果は自由に流れるような形であるべきで、ランドスケープや環境内のアセットから何らかの最小オフセットを持つべきです。",
            
            # Segment 6 (00:02:03 - 00:02:30)
            "How do we do that? What we have to do first is we need to add some pre-processing steps to our supply to make sure that it always conforms to the environment. And the way that I chose to do it for this tutorial is to add more detail to our SP blinds and then move them so that they, you know, don't intersect with the environment here and that they have a minimum offset of, I don't know, So I'm also gonna drop down on no node like.":
            "どうすればよいでしょうか？まず、環境に常に適合するよう、いくつかの前処理ステップを追加する必要があります。このチュートリアルで選択した方法は、スプラインにより多くの詳細を追加し、環境と交差せず、何らかの最小オフセットを持つよう移動させることです。また、ノードを配置します。",
            
            # Segment 7 (00:02:30 - 00:02:52.5)
            "with the environment here so that we have some markers for later when we wanna turn this into a tool that we can share with people. And what I'm gonna do after is to add this detail, I'm gonna get a re-sample node and what it does basically is it just takes the input curve that you have and it re-sample the input it takes whatever you have in there and it adds consistent detail at a rate that we want it.":
            "環境とともに、後でこれを人々と共有できるツールに変換する際のマーカーを持ちます。この詳細を追加した後に行うことは、Resampleノードを取得することです。基本的にこれは入力カーブを取得し、入力を再サンプルして、そこにあるものを取得し、望むレートで一貫した詳細を追加します。",
            
            # Segment 8 (00:02:54 - 00:03:13.5)
            "It's a bit too much for me. It's at 0.1 uh meters. I'm gonna increase it to something like one. Sometimes when I move the value the corner pieces are, you know, being resampled right at that edge and then we can get some deformed splines We can enable this toggle resampled by polygon edge.":
            "少し多すぎます。0.1メートルに設定されています。1メートルくらいに増加させます。値を移動すると、コーナー部分がそのエッジで再サンプルされ、変形したスプラインが得られることがあります。「ポリゴンエッジで再サンプル」のトグルを有効にできます。",
            
            # Segment 9 (00:03:15 - 00:03:37.5)
            "So that's the first step. Now I wanna take care of these intersections and make sure that the curves have this minimum offset on the environment. And what we can do is we can get a ray node and plug in the spline in the left input and the environment in the right input. And what the ray node does is, well it's ray casting our points onto a surface in the right input.":
            "これが最初のステップです。今度は、これらの交差を処理し、カーブが環境に対して最小オフセットを持つようにしたいと思います。Rayノードを取得し、左の入力にスプライン、右の入力に環境を接続します。Rayノードが行うのは、ポイントを右の入力のサーフェスにレイキャスティングすることです。",
            
            # Segment 10 (00:03:36 - 00:03:57)
            "I don't have any directionality though. And what I wanna do instead is I'm just gonna use the closest surface using the minimum distance methods. And now you can see that all our points are snapping to some surface and some of them uh, kind of look, you know, kind of messed up if we look at this well because even though this point is so far away compared to this one, the closest surface might be over here.":
            "方向性はありません。代わりに、最小距離方法を使用して最も近いサーフェスを使用します。すべてのポイントがサーフェスにスナップしているのがわかります。一部は少し乱れて見えます。このポイントがこちらと比較して遠くにあるにも関わらず、最も近いサーフェスがここにある可能性があるためです。",
            
            # Segment 11 (00:03:55.5 - 00:04:18)
            "And so they're all being stretched apart and I don't really want these ones to be affected, the ones that are a bit higher up in the air because what I would wanna do instead is turn those into a hanging bridge. What we can do is we can, we can tell the rain now to prevent some of these points from moving by going a bit further down to the max distance slider over here.":
            "すべてが引き離されており、少し高い位置にあるポイントは影響を受けたくありません。これらを吊り橋にしたいからです。こちらの最大距離スライダーを使用して、これらのポイントの一部が移動しないようRayノードに指示できます。",
            
            # Segment 12 (00:04:16.5 - 00:04:43.5)
            "So if I enable that toggle, you can see everything resets. 'cause we said it's zero, it means none of the points are affected. And so as I start to increase it, you can see that the points like more and more points start to snap to the surface. And this can be a really cool feature because now we can basically tell this Houdini tool, um, that, you know, this could be like the minimum distance that is required for a hang rich spawn,.":
            "このトグルを有効にすると、すべてがリセットされます。ゼロに設定したため、どのポイントも影響を受けません。値を増加させると、より多くのポイントがサーフェスにスナップし始めます。これは非常にクールな機能です。このHoudiniツールに、吊り橋の生成に必要な最小距離を指示できるからです。",
            
            # Segment 13 (00:04:46.5 - 00:05:06)
            "So now we have taken care of the intersections because they're now snapping to the nearest surface. But of course this looks super weird and janky and that's not what we would want, right? We would want them now to be, you know, moved to a, a proper distance. And one way that we can do that is by using the peak note and the peak note.":
            "交差を処理できました。最も近いサーフェスにスナップしているからです。しかし、これは非常に奇妙で不自然に見えます。これは望む結果ではありませんね。適切な距離に移動させたいと思います。Peakノードを使用してこれを行うことができます。",
            
            # Segment 14 (00:05:04.5 - 00:05:24)
            "Basically it just moves points along a direction on the normals. The issue is though that we don't have any normals right now. If I enable the normal preview, we can see yeah, there's nothing on it. The good news is we can get some normals by going to a rain note over here and enabling the point intersection, normal toggle.":
            "基本的に、法線上の方向に沿ってポイントを移動します。問題は、現在法線がないことです。法線プレビューを有効にすると、何もないことがわかります。良いニュースは、こちらのRayノードに行き、ポイント交差の法線トグルを有効にすることで法線を取得できることです。",
            
            # Segment 15 (00:05:24 - 00:05:45)
            "So now we can see that, um, yeah, that every point that has been snapped to the surface is now sampling the You gotta be careful though, with what you're feeding this ray node because in this case this point, for instance, it's right at the corner of a bunch of different polys and it's a very low poly mesh.":
            "サーフェスにスナップした各ポイントがサンプリングしているのがわかります。このRayノードに何を入力するかには注意が必要です。この場合、このポイントは多くの異なるポリゴンのコーナーに位置しており、非常に低ポリのメッシュです。",
            
            # Segment 16 (00:05:43.5 - 00:06:04.5)
            "So the differences can be quite extreme. I guess very likely you will not have an environment that is this low poly. So what we could do is we could just increase the Yeah. And now it looks a bit more normal. Yeah. And when we go back to our peak note now, uh, I'm just gonna disable this recompute point normal so we can see a bit more of what's going on.":
            "差が非常に大きくなる可能性があります。おそらく、このような低ポリの環境を持つことはないでしょう。値を増加させることができます。そして、少し正常に見えます。Peakノードに戻り、「ポイント法線の再計算」を無効にして、何が起こっているかをより確認できるようにします。",
            
            # Segment 17 (00:06:04.5 - 00:06:25.5)  
            "So now if I move this slider of the peak note, we can see that these points are moving along that direction, but the problem is that these points here that we're not affected are moving as well and we don't want that. I would, I want them to be unaffected. Luckily the ray note also can take care of that for us. And if we scroll down, we can see that there's this create point group toggle.":
            "Peakノードのスライダーを移動すると、これらのポイントがその方向に移動しているのがわかります。しかし、影響を受けていないこれらのポイントも移動しており、これは望ましくありません。影響を受けないようにしたいのです。幸い、Rayノードがこれを処理してくれます。下にスクロールすると、「ポイントグループの作成」トグルがあります。",
            
            # Segment 18 (00:06:25.5 - 00:06:48)
            "And if we enable that, we now get this group called re hit group. And this re hit group, as the name kind of suggests, a point group on every point that was affected. And so now if we go to a peak note, we can just go to the group tab and say, Ray hit group. So now these will stay in place and if I keep moving them the other ones, you can see that now we can move them in isolation.":
            "これを有効にすると、「rayhit_group」というグループが得られます。名前が示すように、影響を受けたすべてのポイントのポイントグループです。Peakノードに行き、グループタブで「rayhit_group」を指定します。これらは元の位置に留まり、他のポイントを移動させても、個別に移動できます。",
            
            # Segment 19 (00:06:48 - 00:07:15)
            "So what I would do, what I would recommend you for this kind of tool is that we sync these two values together. The, the max distance value, it would kind of make sense that they have the same kind of, the same kind of distance here. I dunno, it would feel kind of weird to me if we had like this one meter offset, but then the, the hanging bridge So, uh, I would just recommend you to type in the same number or you can also link these two values, these two parameters.":
            "このようなツールで推奨するのは、これら2つの値を同期することです。最大距離値は、同じ種類の距離を持つのが理にかなっています。1メートルのオフセットがあるのに、吊り橋が異なる値だと奇妙に感じます。同じ数値を入力するか、これら2つのパラメータをリンクすることを推奨します。",
            
            # Segment 20 (00:07:15 - 00:07:36)
            "by going uh, copy parameter and go to the peak note and say paste relative reference. And so now if we want to, we can, you know, move the slider on the ray node and the rest adjusts, but I just stick to two meters for now just, um, so it's a bit easier to follow along.":
            "「パラメータをコピー」して、Peakノードに行き「相対参照を貼り付け」を選択します。これで、Rayノードのスライダーを移動すると、残りが調整されます。しかし、フォローしやすくするため、今は2メートルに固定します。",
            
            # Segment 21 (00:07:34.5 - 00:07:55.5)
            "So now we have this roughly prepared spline, but you can very obviously see that um, the density of our points has been suffering a little bit because of the whole projection and and moving it away. And an easy way that we could fix that is by just getting another resample node plugging in the result of what we just did, maybe set it to one meter again.":
            "大まかに準備されたスプラインができました。しかし、投影と移動により、ポイントの密度が少し低下しているのが明らかです。これを修正する簡単な方法は、別のResampleノードを取得して、今行った結果を接続し、再び1メートルに設定することです。",
            
            # Segment 22 (00:07:55.5 - 00:08:15)
            "And then under here where it says treat polygons, I'm gonna say as subdivision curves. That way we also get rid of a little bit of the Jan like here where there's the points are, you know, shooting out a little bit. Yeah, that looks better. Alright.":
            "「ポリゴンの処理」で「サブディビジョンカーブとして」を選択します。これにより、ポイントが少し突き出ているような部分の不自然さも取り除かれます。こちらの方が良く見えます。よし。",
            
            # Segment 23 (00:08:15 - 00:08:33)
            "And now comes the first step of what we wanna do with this tool and that is that, you know, the most important thing obviously are these wooden planks that are, um, scattered all over the place and they are in fact scattered and we need to create points for this.":
            "このツールで行いたいことの最初のステップです。最も重要なことは、あちこちに散らばっている木製板材です。これらは実際に散らばっており、このためのポイントを作成する必要があります。",
            
            # Segment 24 (00:08:33 - 00:09:00)
            "The whole thing about this tool is that everything is just scattered. It's just points with some information about where something is, how large it is, in which direction it's pointing. All of this information we can store on these little points over here. And that is something really cool and powerful that Houdini is really good at by using our attributes that we can find in the geometry spreadsheet.":
            "このツールの重要な点は、すべてが単に散布されているということです。これは単に、何かがどこにあるか、どのくらい大きいか、どの方向を向いているかの情報を持つポイントです。この情報はすべて、これらの小さなポイントに保存できます。これは、ジオメトリスプレッドシートで見つけることができるアトリビュートを使用して、Houdiniが非常に得意とする、クールで強力な機能です。",
            
            # Segment 25 (00:08:58.5 - 00:09:24)
            "So how do we get started? Well, what I would like to do is I would like to, uh, separate the individual parts of this plan based on certain rules that I thought would make sense. Of course you can come up with any kind of other rules, but I thought, you know, what would make sense is that we have the, this very basic group that is just, um, general planks that you walk on.":
            "どのように始めればよいでしょうか？理にかなうと思われる特定のルールに基づいて、この計画の個別部分を分離したいと思います。もちろん、他のルールを思いつくことができますが、基本的なグループ、つまり歩行用の一般的な板材があると良いと考えました。",
            
            # Segment 26 (00:09:22.5 - 00:09:49.5)
            "Then we have on, uh, in areas that are higher than this maximum distance for our bridge. They get turned into a hanging bridge and then we treat this part of the spline differently, make it, make it hang down a random amount. And if we have especially steep areas such as this one, if we calculate the incline of this spline, we could treat it as a staircase and you know, make all the planks be pointing upwards so.":
            "橋の最大距離よりも高い領域では、吊り橋に変換し、このスプライン部分を異なって処理して、ランダムな量だけ垂れ下がらせます。このような特に急な領域がある場合、このスプラインの傾斜を計算し、階段として処理し、すべての板材を上向きにして、",
            
            # Segment 27 (00:09:49.5 - 00:10:07.5)
            "that we have something to stand on. I think the first thing I wanna start with is the hanging bridge because it has a large impact and I think it, it kind of gets the whole ball rolling. Um, and what I need for that is I need to know how far away each of these points is from the nearest surface and we can just get another rain note for that.":
            "立つことができる何かを用意します。最初に始めたいのは吊り橋です。大きな影響があり、全体の流れを作り出すと思います。そのために必要なのは、これらの各ポイントが最も近いサーフェスからどのくらい離れているかを知ることで、そのために別のRayノードを取得できます。",
            
            # Segment 28 (00:10:07.5 - 00:10:27)
            "And I'm, I mean we could also start this on this ray node, but I just wanna make sure that I have the most accurate uh, reading and that's why I'm just gonna get another one. So let's just plug that in and I'm gonna choose the minimum distance setting again, but this time I don't want any of the points to move.":
            "このRayノードでも開始できますが、最も正確な読み取りを確保したいため、別のノードを取得します。接続して、再び最小距離設定を選択しますが、今回はポイントを移動させたくありません。",
            
            # Segment 29 (00:10:27 - 00:10:52.5)
            "I just want to sample some data. We can do that by disabling this transform points toggle over here and instead I'm just gonna enable this here, this point intersection distance toggle. And now we can see if you looked down here on my geometry spreadsheet, it is adding an attribute called this and this, this attribute as the name kind of suggests is for each point it's reading, it's sampling the distance.":
            "データをサンプリングしたいだけです。「ポイントの変形」トグルを無効にし、代わりに「ポイント交差距離」トグルを有効にします。ジオメトリスプレッドシートを見ると、「dist」という属性が追加されています。名前が示すように、この属性は各ポイントで距離をサンプリングしています。",
            
            # Segment 30 (00:10:54 - 00:11:16.5)
            "And this is some incredibly valuable information that we have available to us now. So because we can check this spreadsheet against this value that we have over here, the max distance, we can say, hey, if it's higher than two meters, like 2.1, let's say, um, we can say that you are probably a rich and then we separate this part of our spine and send it to a different part of our graph.":
            "これは非常に価値のある情報です。このスプレッドシートを最大距離値と照合できるため、2.1メートルなど2メートルより高い場合は、おそらく吊り橋であり、スプラインのこの部分を分離してグラフの異なる部分に送ることができます。",
            
            # 追加のセグメント翻訳はここに続く...
            # より多くのセグメントを翻訳する場合は、同様のパターンで追加
        }

    def translate_subtitle_segment(self, segment_text):
        """個別セグメントの翻訳"""
        # 完全一致での翻訳を優先
        if segment_text in self.comprehensive_translations:
            return self.comprehensive_translations[segment_text]
        
        # 部分一致または基本翻訳を使用
        return self.basic_translation(segment_text)
    
    def basic_translation(self, text):
        """基本翻訳（フォールバック）"""
        # 基本的な単語置換
        basic_terms = {
            "spline": "スプライン",
            "curve": "カーブ", 
            "node": "ノード",
            "points": "ポイント",
            "bridge": "橋",
            "tool": "ツール",
            "geometry": "ジオメトリ"
        }
        
        result = text
        for eng, jp in basic_terms.items():
            result = result.replace(eng, jp)
        
        return result

    def translate_translation_queue(self, queue_data):
        """翻訳キュー全体の処理"""
        translated_data = {
            "chapter_info": {
                "number": queue_data["chapter_info"]["number"],
                "title": "基本ロジック",
                "duration_seconds": queue_data["chapter_info"]["duration_seconds"],
                "video_id": queue_data["chapter_info"]["video_id"]
            },
            "subtitle_segments": [],
            "learning_segments": queue_data["learning_segments"],  # 学習セグメントはそのまま使用
            "technical_metadata": queue_data["technical_metadata"]
        }
        
        # 字幕セグメントの翻訳
        for segment in queue_data["subtitle_segments"]:
            translated_segment = {
                "id": segment["id"],
                "start": segment["start"],
                "end": segment["end"],
                "text": self.translate_subtitle_segment(segment["text"])
            }
            translated_data["subtitle_segments"].append(translated_segment)
        
        return translated_data

def main():
    if len(sys.argv) != 2:
        print("使用方法: python comprehensive_subtitle_translator.py <translation_queue.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 入力ファイルのパス解決
    if not os.path.isabs(input_file):
        base_dir = Path(__file__).parent.parent / "tutorials" / "Project_Skylark_Bridges" / "05_translation_batch"
        input_path = base_dir / input_file
    else:
        input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"エラー: ファイル {input_path} が見つかりません")
        sys.exit(1)
    
    # 翻訳実行
    translator = ComprehensiveSubtitleTranslator()
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            queue_data = json.load(f)
        
        translated_data = translator.translate_translation_queue(queue_data)
        
        # 出力ファイル名生成
        output_filename = input_path.stem.replace('_queue', '_queue_comprehensive_jp') + '.json'
        output_path = input_path.parent / output_filename
        
        # 翻訳データ保存
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=2)
        
        print(f"包括的字幕翻訳完了: {output_path}")
        print(f"処理された字幕セグメント数: {len(translated_data['subtitle_segments'])}")
        
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()