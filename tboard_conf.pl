#
#  v �Ķ�����ե�����
#
sub conf {

    my %conf;

    chomp($conf{title} = <<'_title_str_');
�ĥ꡼�ܡ��ɥƥ�����
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
�ǽ��쥹����������θŤ���Τ���
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
���� ���� ���� �Ҥߤ�
_sexstr_str_
    chomp($conf{prefstr} = <<'_prefstr_str_');
���� ���� ���� �Ҥߤ� �̳�ƻ �Ŀ��� ��긩 �ܾ븩 ���ĸ� ������ ʡ�縩 ��븩 ���ڸ� ���ϸ� ��̸� ���ո� ����� ����� ������ Ĺ� ���㸩 �ٻ��� ��� ʡ�温 ���츩 �Ų��� ���θ� ���Ÿ� ���츩 ������ ����� ʼ�˸� ���ɸ� �²λ��� Ļ�踩 �纬�� ������ ���縩 ������ ���縩 ��� ��ɲ�� ���θ� ʡ���� ���츩 Ĺ�긩 ���ܸ� ��ʬ�� �ܺ긩 �����縩 ���츩 ����
_prefstr_str_
    chomp($conf{agestr} = <<'_agestr_str_');
���ɤ� ��ǯ ���� ��� ��ǯ ���� 10�� 20�� 30�� 40�� 50�� 60��ʾ�
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
<font color=red>[���!]</font>
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
���(�֥롼)
��ϤϤ�(�֥롼)
�勞�勞(�֥롼)
��������(�֥롼)
�����(�֥롼)
�פ�(�֥롼)
������(�֥롼)
���꤬��(�֥롼)
Zzzz...(�֥롼)
�ˤ��(�֥롼)
����(�֥롼)
���뤡��(�֥롼)
������(�֥롼)
�ݤ�(�֥롼)
���(�ԥ�)
��ϤϤ�(�ԥ�)
�勞�勞(�ԥ�)
��������(�ԥ�)
�����(�ԥ�)
�פ�(�ԥ�)
������(�ԥ�)
���꤬��(�ԥ�)
Zzzz...(�ԥ�)
�ˤ��(�ԥ�)
����(�ԥ�)
���뤡��(�ԥ�)
������(�ԥ�)
�ݤ�(�ԥ�)
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
