#
#  v 環境設定ファイル
#
sub conf {

    my %conf;

    chomp($conf{title} = <<'_title_str_');
ツリーボードテスト中
_title_str_
    chomp($conf{title_img} = <<'_title_img_str_');

_title_img_str_
    chomp($conf{title_align} = <<'_title_align_str_');
left
_title_align_str_
    chomp($conf{description} = <<'_description_str_');

_description_str_
    chomp($conf{script_url} = <<'_script_url_str_');
http://test.psl.ne.jp/_psl/tboard01/tboard.cgi
_script_url_str_
    chomp($conf{home_url} = <<'_home_url_str_');
http://www.psl.ne.jp/
_home_url_str_
    chomp($conf{k_email} = <<'_k_email_str_');
iwanami@psl.ne.jp
_k_email_str_
    chomp($conf{tree_max} = <<'_tree_max_str_');
100
_tree_max_str_
    chomp($conf{del_tree_method} = <<'_del_tree_method_str_');
最終レスの投稿日時の古いものから
_del_tree_method_str_
    chomp($conf{page_disp_tree} = <<'_page_disp_tree_str_');
10
_page_disp_tree_str_
    chomp($conf{page_disp_thread} = <<'_page_disp_thread_str_');
5
_page_disp_thread_str_
    chomp($conf{page_disp_list} = <<'_page_disp_list_str_');
15
_page_disp_list_str_
    chomp($conf{page_disp_list2} = <<'_page_disp_list2_str_');
10
_page_disp_list2_str_
    chomp($conf{page_disp_topic} = <<'_page_disp_topic_str_');
15
_page_disp_topic_str_
    chomp($conf{subject_length} = <<'_subject_length_str_');
70
_subject_length_str_
    chomp($conf{color} = <<'_color_str_');
#333333 blue #6666ff green darkgreen brown darkorange purple
_color_str_
    chomp($conf{admin_color} = <<'_admin_color_str_');
red
_admin_color_str_
    chomp($conf{sexstr} = <<'_sexstr_str_');
男性 女性 中性 ひみつ
_sexstr_str_
    chomp($conf{prefstr} = <<'_prefstr_str_');
職場 自宅 客先 ひみつ 北海道 青森県 岩手県 宮城県 秋田県 山形県 福島県 茨城県 栃木県 群馬県 埼玉県 千葉県 東京都 神奈川県 山梨県 長野県 新潟県 富山県 石川県 福井県 岐阜県 静岡県 愛知県 三重県 滋賀県 京都府 大阪府 兵庫県 奈良県 和歌山県 鳥取県 島根県 岡山県 広島県 山口県 徳島県 香川県 愛媛県 高知県 福岡県 佐賀県 長崎県 熊本県 大分県 宮崎県 鹿児島県 沖縄県 海外
_prefstr_str_
    chomp($conf{agestr} = <<'_agestr_str_');
こども 少年 少女 若者 青年 乙女 10代 20代 30代 40代 50代 60代以上
_agestr_str_
    chomp($conf{body_text} = <<'_body_text_str_');
#333333
_body_text_str_
    chomp($conf{body_bgcolor} = <<'_body_bgcolor_str_');
#ffffff
_body_bgcolor_str_
    chomp($conf{body_link} = <<'_body_link_str_');
#3333ff
_body_link_str_
    chomp($conf{body_alink} = <<'_body_alink_str_');
#ffffcc
_body_alink_str_
    chomp($conf{body_vlink} = <<'_body_vlink_str_');
#0000ff
_body_vlink_str_
    chomp($conf{body_background} = <<'_body_background_str_');

_body_background_str_
    chomp($conf{stylesheet} = <<'_stylesheet_str_');
  body,pre,td,th { font-size: 10.5pt; }
  tt { font-size: 12pt; }
  a {text-decoration: none;}
  a:hover { color:red; text-decoration:underline; }
  .message_subject { font-size: 12pt; }
  .message_smallfont { font-size: 9.5pt; }
_stylesheet_str_
    chomp($conf{opt_age} = <<'_opt_age_str_');
0
_opt_age_str_
    chomp($conf{opt_sex} = <<'_opt_sex_str_');
0
_opt_sex_str_
    chomp($conf{opt_pref} = <<'_opt_pref_str_');
0
_opt_pref_str_
    chomp($conf{opt_email_mode} = <<'_opt_email_mode_str_');
1
_opt_email_mode_str_
    chomp($conf{opt_notify} = <<'_opt_notify_str_');
1
_opt_notify_str_
    chomp($conf{opt_url} = <<'_opt_url_str_');
1
_opt_url_str_
    chomp($conf{opt_solved} = <<'_opt_solved_str_');
0
_opt_solved_str_
    chomp($conf{opt_solved_str} = <<'_opt_solved_str_str_');
<font color=red>[解決!]</font>
_opt_solved_str_str_
    chomp($conf{opt_message2} = <<'_opt_message2_str_');
0
_opt_message2_str_
    chomp($conf{opt_cid} = <<'_opt_cid_str_');
1
_opt_cid_str_
    chomp($conf{opt_icon} = <<'_opt_icon_str_');
1
_opt_icon_str_
    chomp($conf{icon_list} = <<'_icon_list_str_');
a_0001.gif
a_0002.gif
a_0003.gif
a_0004.gif
a_0005.gif
a_0006.gif
a_0007.gif
a_0008.gif
a_0009.gif
a_0010.gif
a_0011.gif
a_0012.gif
a_0013.gif
a_0014.gif
b_0001.gif
b_0002.gif
b_0003.gif
b_0004.gif
b_0005.gif
b_0006.gif
b_0007.gif
b_0008.gif
b_0009.gif
b_0010.gif
b_0011.gif
b_0012.gif
b_0013.gif
b_0014.gif
_icon_list_str_
    chomp($conf{icon_list_str} = <<'_icon_list_str_str_');
わーい(ブルー)
わははは(ブルー)
わくわく(ブルー)
うぇーん(ブルー)
ちゅっ(ブルー)
ぷん(ブルー)
ごめんね(ブルー)
ありがと(ブルー)
Zzzz...(ブルー)
にやり(ブルー)
冷や汗(ブルー)
ごるぁぁ(ブルー)
らんらん♪(ブルー)
ぽっ(ブルー)
わーい(ピンク)
わははは(ピンク)
わくわく(ピンク)
うぇーん(ピンク)
ちゅっ(ピンク)
ぷん(ピンク)
ごめんね(ピンク)
ありがと(ピンク)
Zzzz...(ピンク)
にやり(ピンク)
冷や汗(ピンク)
ごるぁぁ(ピンク)
らんらん♪(ピンク)
ぽっ(ピンク)
_icon_list_str_str_
    chomp($conf{new_mark} = <<'_new_mark_str_');
12
_new_mark_str_
    chomp($conf{new_mark_str} = <<'_new_mark_str_str_');
<img src="img/new.gif" alt="NEW!" border=0>
_new_mark_str_str_
    chomp($conf{up_mark_str} = <<'_up_mark_str_str_');
<img src="img/up.gif" alt="UP!" border=0>
_up_mark_str_str_
    chomp($conf{mailsend} = <<'_mailsend_str_');
smtp
_mailsend_str_
    chomp($conf{sendmail} = <<'_sendmail_str_');
/usr/sbin/sendmail
_sendmail_str_
    chomp($conf{smtp} = <<'_smtp_str_');
ns.psl.ne.jp
_smtp_str_
    %conf;

}

1;
