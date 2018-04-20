# -*- coding: utf8 -*-
import re

REMOVE_TAGS = [
    'div', 'img', 'a', 'br', 'h4',
    'blockquote', 'tr', 'td', 'span', 'p', 'h3'
]

REMOVE_WHOLE = [
    "script", "font"
]

def removeHtml(doc):
    result = doc
    pattern = r"<%s.*?>"
    pattern2 = r"</%s.*?>"
    for tag in REMOVE_TAGS:
        result = re.sub(pattern%tag, "", result)
        result = re.sub(pattern2%tag, "", result)
    return re.sub(r"\s+", " ", result).strip()

def removeWhole(doc):
    result = doc
    pattern = r"<%s[\s\S]*?<\/%s>"
    for tag in REMOVE_WHOLE:
        result = re.sub(pattern%(tag, tag), "", result)
    return re.sub(r"\s+", " ", result).strip()

def removeFloor(doc):
    pattern = ur"\d*?楼\.\s?"
    result = re.sub(pattern, "", doc, flags=re.UNICODE)
    return re.sub(r"\s+", " ", result).strip()

def removeAll(doc):
    return removeFloor(removeWhole(removeHtml(doc)))

if __name__ == '__main__':
    doc = """<td class="c2" id="postcontainer12" style="vertical-align:top">
         <a id="pid263247081Anchor">
         </a>
         <a name="l12">
         </a>
         <div class="postBtnPos" id="postBtnPos12">
         </div>
         <div class="postInfo" id="postInfo12">
          <span id="postdate12" title="reply time">
           11楼. 2018-02-11 00:00
          </span>
         </div>
         <span id="postcontentandsubject12">
          <h3 id="postsubject12">
          </h3>
          <br>
          <span class="postcontent ubbcode" id="postcontent12">
           丰年是什么活动？萌新
          </span>
          <br>
         </span>
         <div class="clear">
         </div>
         <div class="x" id="postsign12">
         </div>
         <script>
          commonui.postArg.proc( 12,
$('postcontainer12'),$('postsubject12'),$('postcontent12'),$('postsign12'),$('posterinfo12'),$('postInfo12'),$('postBtnPos12'),
null,null,263247081,512,
null,'42639060',1518278424,'0,0,0','20',
'','','7 iPhone 6(iOS 11.2.5)','',null,0 )
         </script>
        </td>
    """
    doc2 = """<div class="i">
     12楼.
     <a href="http://c.hiphotos.baidu.com/forum/w%3D400%3Bq%3D80%3Bg%3D0/sign=09ab1a1d9116fdfad86cc7ee84b4fd69/2494c14ad11373f02c468ea9a80f4bfbfaed04e0.jpg?&amp;src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2F2494c14ad11373f02c468ea9a80f4bfbfaed04e0.jpg">
      <br>
      <img class="BDE_Image" src="http://c.hiphotos.baidu.com/forum/w%3D96%3Bq%3D45%3Bg%3D0/sign=177c4f5643c2d562f208dcebdc60addb/2494c14ad11373f02c468ea9a80f4bfbfaed04e0.jpg?&amp;src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2F2494c14ad11373f02c468ea9a80f4bfbfaed04e0.jpg">
      <br>
     </a>
     <br>
     </div>
    """
    print removeAll(doc2)
