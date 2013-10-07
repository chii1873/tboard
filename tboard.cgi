#!/usr/bin/perl -Tw
# ---------------------------------------------------------------
#  - システム名    Tree Board
#  - バージョン    0.1
#  - 公開年月日    2004/10/10
#  - スクリプト名  tboard.cgi
#  - 著作権表示    (c)1997-2004 Perl Script Laboratory
#  - 連  絡  先    info@psl.ne.jp (http://www.psl.ne.jp/)
# ---------------------------------------------------------------
# ご利用にあたっての注意
#   ※このシステムはフリーウエアです。
#   ※このシステムは、「利用規約」をお読みの上ご利用ください。
#     http://www.psl.ne.jp/lab/copyright.html
# ---------------------------------------------------------------
use strict;
use vars qw(%FORM %CONF %tables $LOCKED $smtp);
use CGI::Carp qw(fatalsToBrowser);
require 'jcode.pl';
%CONF = setver();
_init();
umask 0;
$ENV{TZ} = 'JST-9';
$ENV{PATH} = "/usr/bin:/usr/sbin:/usr/local/bin:/bin";
if (-e './tboard_conf.pl') {
    require './tboard_conf.pl';
    %CONF = (%CONF, conf());
} else {
    init_setup();
    init_passwd_file();
    setup("init");
}

my $q;
if ($CONF{img_upload}) {
    eval { use CGI qw(param uploadInfo); };
    error("CGIモジュールのインポートができませんでした。: $@") if $@;
    $q = new CGI;
}
%FORM = decoding($q);

login()       if $FORM{login};
admin()       if $FORM{admin};
chpasswd()    if $FORM{chpasswd};
chpasswd2()   if $FORM{chpasswd2};
com()         if $FORM{com} or $FORM{mod};
com_confirm() if $FORM{com_confirm};
com_done()    if $FORM{com_done};
cookie_mod()  if $FORM{cookie_mod};
cookie_mod_done() if $FORM{cookie_mod_done};
del()         if $FORM{del};
del_confirm() if $FORM{del_no};
logout()      if $FORM{logout};
mailform()    if $FORM{mailform};
mailform_done() if $FORM{mailform_done};
setup()       if $FORM{setup};
setup2()      if $FORM{setup2};
view2()       if $FORM{view2};
view_icon()   if $FORM{view_icon};
view();
exit;

sub _init {

    %tables = (
        "tboard_tree.cgi" => [qw(tno reg_date last_update message_cnt)],
        "tboard_message.cgi" => [qw(msgno tno pno indent stat reg_date
          last_update userid passwd cid name age sex pref subject
          subject_color email url message message_color parent_message_color
          message2 pre do_link solved email_mode notify icon remote_host
          user_agent)],
    );

    %CONF = (%CONF,
	hl_bgcolor => q{#ffcccc},
	prev0str => q{<font color=#999999>&lt;&lt; 前ページ</font>},
	prev1str => q{&lt;&lt; 前ページ},
	next0str => q{<font color=#999999>次ページ &gt;&gt;</font>},
	next1str => q{次ページ &gt;&gt;},
	script_name => q{tboard.cgi},
	tempfile_del_hour => 6,
	cookie_expire_days => 30,
	write_conf_fields => [qw(title title_color title_font_size
	 title_is_bold title_img title_align description script_url home_url
	 k_email tree_max del_tree_method page_disp_tree page_disp_thread
	 page_disp_list page_disp_list2 page_disp_topic subject_length color
	 admin_color sexstr prefstr agestr body_text body_bgcolor body_link
	 body_alink body_vlink body_background stylesheet opt_age opt_sex
	 opt_pref opt_email_mode opt_notify opt_url opt_solved opt_solved_str
	 opt_message2 opt_cid opt_icon icon_list icon_list_str new_mark
	 new_mark_str up_mark_str mailsend sendmail smtp)],
	session_data_fields => [qw(msgno pno passwd cid name age sex pref
	  subject subject_color email url message message_color
          message2 pre do_link solved email_mode notify icon remote_host
          user_agent)],
	cookie_fields => [qw(name passwd sex age pref email email_mode notify
	 url subject_color message_color disp_type_default
	 page_disp_tree page_disp_thread page_disp_list page_disp_list2
	 page_disp_topic icon)],
	list_header => {
	  list => qq{<table border=0 cellpadding=0 cellspacing=0 width=700 bgcolor="##body_text##"><tr><td><table border=0 cellpadding=5 cellspacing=1 width=100%>\n<tr><td bgcolor=##body_bgcolor## width=390 align=center>件　　名</td><td bgcolor=##body_bgcolor## width=160 align=center>投稿者</td><td bgcolor=##body_bgcolor## align=center width=140>投稿日時</td></tr>\n},
	  topic => qq{<table border=0 cellpadding=0 cellspacing=0 width=700 bgcolor="##body_text##"><tr><td><table border=0 cellpadding=5 cellspacing=1 width=100%>\n<tr><td bgcolor=##body_bgcolor## width=350 align=center>件　　名</td><td bgcolor=##body_bgcolor## width=150 align=center>投稿者</td><td bgcolor=##body_bgcolor## align=center width=140>投稿日時</td><td bgcolor=##body_bgcolor## align=center width=50>投稿数</td></tr>\n},
	},
	list_footer => {
	  list => qq{</td></tr></table></td></tr></table><p>\n},
	  topic => qq{</td></tr></table></td></tr></table><p>\n},
	},
    );
    ($ENV{REQUEST_URI}) = (split(/\?/, $ENV{REQUEST_URI}))[0];
    $CONF{script_url} ||= "http://$ENV{SERVER_NAME}$ENV{REQUEST_URI}";
    chomp($CONF{tree_format} = <<'STR');
##subject##<span style="font-size:7.5pt;"> (##msgno##)</span><span style="font-size:9pt;"> ##name## - ##reg_date##</span>##new####up##
STR
    chomp($CONF{list_format} = <<'STR');
<tr>
<td bgcolor=##body_bgcolor## width=390>##subject##<span style="font-size:7.5pt;"> (##msgno##)</span>##new####up##</td>
<td bgcolor=##body_bgcolor## width=160>##name##</td>
<td bgcolor=##body_bgcolor## align=center width=140>##reg_date##</td>
</tr>
STR
    chomp($CONF{topic_format} = <<'STR');
<tr>
<td bgcolor=##body_bgcolor## width=370>##subject####new####up##</td>
<td bgcolor=##body_bgcolor## width=150>##name##</td>
<td bgcolor=##body_bgcolor## align=center width=140>##reg_date##</td>
<td bgcolor=##body_bgcolor## align=right width=30>##message_cnt##</td>
</tr>
STR
    $CONF{message_permission} = $CONF{script_name} . q{を設置したディレクトリのパーミッションが707(suExecなどの環境の場合は700など)になっているか確認してください。};
}

sub _admin_header {

    my $subtitle = shift;
    return <<STR;
Content-type: text/html; charset=euc-jp

<html><head><title>$CONF{prod_name} v$CONF{version} $subtitle</title>
<meta name="robots" content="noindex, nofollow">
<style type="text/css">
  body,pre,td,th { font-size: 10.5pt; line-height:120%; }
  textarea { font-size: 10.5pt; }
  a {text-decoration: none;}
  a:hover { color:red; text-decoration:underline; }
  .smallfont { font-size: 9.5pt; }
</style>
</head>
<body text="$CONF{body_text}" bgcolor="$CONF{body_bgcolor}"
link="$CONF{body_link}" vlink="$CONF{body_vlink}" alink="$CONF{body_alink}"
background="$CONF{body_background}">
<div align=center>
<table width=700><tr><td>
<h3>$CONF{prod_name} v$CONF{version} $subtitle</h3>
STR

}

sub _cookie_mod_html {

    open(R, "_cookie_mod.html") or error(__LINE__);
    return join("", <R>);

}

sub _footer {

    my $opt = shift;
    my $border = $opt eq "no_border" ? "" : "<hr noshade>";
    return <<STR;
$border
<div align=right><b><span style="font-size:9pt"><a href=$CONF{a_url} target=_top>$CONF{prod_name} v$CONF{version}</a></span></b></div>
</form></td></tr></table></div></body></html>
STR

}

sub _form_html {

    open(R, $_[0] ? "_mod.html" : "_com.html") or error(__LINE__);
    return join("", <R>);

}

sub _header {

    my $subtitle = shift;

    my $bold = $CONF{title_is_bold} ? "font-weight:bold;" : "";
    my $title = $CONF{title_img} ? qq{<img src="$CONF{title_img}" alt="$CONF{title}">} : qq{<span style="color:$CONF{title_color};font-size:$CONF{title_font_size}pt;$bold">$CONF{title}</span>};

#    my $admin_str = admin_str(get_cookie('TBOARD_ADMIN'));
    return <<STR;
Content-type: text/html; charset=euc-jp

<html><head><title>$CONF{title} - $subtitle</title>
<style>
.description { font-size: 9.5pt; }
$CONF{stylesheet}
</style>
</head>

<body text="$CONF{body_text}" bgcolor="$CONF{body_bgcolor}"
link="$CONF{body_link}" vlink="$CONF{body_vlink}" alink="$CONF{body_alink}"
background="$CONF{body_background}">
<div align=center>
<form action=$CONF{script_name} method=post>
<table border=0 cellpadding=0 cellspacing=0 width=700>
<tr><td align=$CONF{title_align}>$title </td></tr></table>

<table><tr><td></td></tr></table>

<table width=700><tr><td>
<b>$subtitle</b>
STR

}

sub _mailform_html {

    open(R, "_mailform.html") or error(__LINE__);
    return join("", <R>);

}

sub _setup_html {

    open(R, "_setup.html") or error(__LINE__);
    return join("", <R>);

}

sub _view2_html {

    open(R, "_view2.html") or error(__LINE__);
    return join("", <R>);

}

sub admin {

    login_check();

    print _admin_header("管理メニュー");
    print <<HTML;
<table border cellpadding=3 cellspacing=0 width=660>
<tr><th width=140><a href=$CONF{script_name}>管理モード閲覧</a></th>
<td><span class=smallfont>管理者モードで掲示板を閲覧することができます。</span></td></tr>
<tr><th><a href=$CONF{script_name}?chpasswd>パスワード変更</a></th>
<td><span class=smallfont>管理人用パスワードの変更ができます。</span></td></tr>
<tr><th><a href=$CONF{script_name}?setup>環境設定</a></th>
<td><span class=smallfont>このシステムの諸設定を変更できます。設定データは環境設定ファイルに書き込まれます。</span></td></tr>
<tr><th><a href=$CONF{script_name}?logout>ログアウト</a></th>
<td><span class=smallfont>クッキーデータを消去し、ログアウトします。</span></td></tr>
</table>
HTML
    print _footer();

    exit;

}


sub admin_str {

    my($admin_passwd) = @_;

    if ($admin_passwd ne '') {
        return <<STR;
<table border=0 cellpadding=0 cellspacing=0 bgcolor=#ddddaa>
<tr><td>[管理モード]　　<a href=$CONF{script_name}?admin>管理メニューへ</a></td></tr>
</table>
STR

    }
    undef;
}

sub autolink_email {

    my($str) = shift;
    $str =~ s#([-_.!*a-zA-Z0-9/&+%\#]+\@[-_.a-zA-Z0-9]+\.(?:[a-zA-Z]{2,3}))#<a href="mailto:$1">$1</a>#g;
    return $str;

}

sub autolink_url {

    my($str, $target) = shift;
    if ($target ne "") {
        $target = qq{target="$target"};
    }
    $str =~ s#(s?https?://[-_.!~*'()a-zA-Z0-9;/?:\@&=+\$,%\#]+)#<a href="$1" $target>$1</a>#g;
    return $str;

}

sub base64_encode {

    my($subject) = @_;
    my($str, $padding);
    while ($subject =~ /(.{1,45})/gs) {
        $str .= substr(pack('u', $1), 1);
        chop($str);
    }
    $str =~ tr|` -_|AA-Za-z0-9+/|;
    $padding = (3 - length($subject) % 3) % 3;
    $str =~ s/.{$padding}$/'=' x $padding/e if $padding;
    $str;

}

sub base64_decode {

    my $str = shift;
    my $res = "";

    $str =~ tr|A-Za-z0-9+=/||cd;
    if (length($str) % 4) {
        error("デコード対象の文字列が不正です。: $str");
    }
    $str =~ s/=+$//;
    $str =~ tr|A-Za-z0-9+/| -_|;
    while ($str =~ /(.{1,60})/gs) {
	my $len = chr(32 + length($1) * 3 / 4);
	$res .= unpack("u", $len . $1 );
    }
    $res;
}

sub chpasswd {

    login_check();

    print _admin_header("パスワード変更");
    print <<HTML;
<a href=$CONF{script_name}?admin><b>管理メニューへ</b></a><p>
<form action=$CONF{script_name} method=post>
管理用パスワードを変更します。変更したいパスワードを入力してください。<br>
パスワードは半角英数字8文字以内で指定してください。<p>

<input type=password name=new_passwd size=13 style="ime-mode:inactive;"><p>

確認のため、もう一度入力してください。<p>

<input type=password name=new_passwd_again size=13 style="ime-mode:inactive;"><p>

<input type=submit name=chpasswd2 value="パスワードを変更する">
</form>
</ul>
HTML
    print _footer();

    exit;

}

sub chpasswd2 {

    login_check();

    if ($FORM{new_passwd} eq '') {
        error('新しいパスワードが入力されていません。');
    }
    if ($FORM{new_passwd} =~ /\W/) {
        error('パスワードは半角英数字のみで指定してください。');
    }
    if ($FORM{new_passwd} ne $FORM{new_passwd_again}) {
        error('入力された2つのパスワードが同一でありません。');
    }
    if (length($FORM{new_passwd}) > 8) {
        error('パスワードは半角英数字8文字以内で指定してください。');
    }

    open(W, "> tboard_passwd.cgi")
     or error("パスワードファイルへの書き出しに失敗しました。: $!");
    print W crypt_passwd($FORM{new_passwd});
    close(W);

    if (get_cookie("TBOARD_ADMIN_CACHE")) {
        set_cookie("TBOARD_ADMIN_CACHE", 30, $FORM{new_passwd});
    }
    print "Location: $CONF{script_name}?admin\n\n";
    exit;

}

sub cid_required {

    if ($CONF{opt_cid}) {
        my $cid = get_cookie("TBOARD_CID")
         or error("cookie-IDが書き込めません。ブラウザのcookie機能を有効にしてください。");
        return $cid;
    }

}

sub com {

    # エラーメッセージがある場合は%FORMの値を優先する
    my $error_ref = shift;
    my %data;
    my $errmsg;
    if ($error_ref) {
        $errmsg = join("", map { "<li>$_\n" } @$error_ref);
    }
    # クッキーデータ/セッションデータをロード
    %data = cookie_data_decode(get_cookie('TBOARD'));
    if ($FORM{sid}) {
        %data = (%data, session_data("get", $FORM{sid}));
        $FORM{pno} = $data{pno};
    } elsif ($FORM{msgno}) {
        my $p = table_select("tboard_message.cgi","msgno=$FORM{msgno}");
        $p->{msgno} or error("該当する発言データがありませんでした。");
        %data = (%data, %$p);
        $data{msgno} = $FORM{msgno};
    }
    # cookie-IDチェック
    $data{cid} = cid_required() if $CONF{opt_cid};

    $data{url} ||= 'http://';
    $data{email_mode} = 1 if $data{email_mode} eq '';

    my %str = get_comform_str(%data);

    my $com_type;
    if ($FORM{pno}) {
        my $p = table_select("tboard_message.cgi","msgno=$FORM{pno}");
        $p->{msgno} or error("該当する発言データがありませんでした。");
        if (!$FORM{sid}) {
            $p->{message} =~ s/\n/\n> /g;
            $data{message} = "> $p->{message}";
            $data{subject} = $p->{subject};
            if ($data{subject} =~ /^re: *\D*/i) {
                $data{subject} =~ s/^re: */Re\^2: /i;
            } elsif ($data{subject} =~ /^re\^(\d*): */i) {
                $data{subject} =~ s/^re\^(\d*): */"Re\^".($1+1).": "/ei;
            } else {
                $data{subject} = 'Re: ' . $data{subject};
            }
            $data{do_link} = 1 if $p->{do_link};
            $data{pre} = 1 if $p->{pre};
            $data{pno} = $FORM{pno};
            $data{sid} = $FORM{sid} = gen_sid();
            session_data("set", $data{sid}, \%data);
        }
        $com_type = qq{No.$p->{msgno}「$p->{subject}」(投稿者：$p->{name})}.
         qq{への返信};
    } else {
        $com_type = qq{新規投稿};
    }
    if ($FORM{msgno}) {
        $com_type = "投稿済み記事の修正";
    }

    my $htmlstr = _form_html($FORM{msgno});
    foreach (qw(age sex pref email_mode notify url solved solved_str
     message2 icon)) {
        unless ($CONF{"opt_$_"}) {
            $htmlstr =~ s/<!-- opt_${_}_begin -->/<!--/ig;
            $htmlstr =~ s/<!-- opt_${_}_end -->/-->/ig;
        }
    }
    foreach (qw(sex pref age subject_color message_color icon)) {
        $htmlstr =~ s/##${_}list##/$str{$_}/g;
    }
    foreach (qw(body_text body_bgcolor body_link)) {
        $htmlstr =~ s/##$_##/$CONF{$_}/g;
    }
    foreach my $f(qw(notify do_link pre)) {
        $htmlstr =~ s/##$f:([^#]+)##/$1 eq $data{$f} ? "checked" : ""/eg;
    }

    $htmlstr =~ s/##navi_bar##/mk_navi_bar(0,%FORM)/e;
    $htmlstr =~ s/##sid##/$FORM{sid}/g;
    $htmlstr =~ s/##cid##/$data{cid}?"[ID:$data{cid}]":""/eg;
    $htmlstr =~ s/##email_mode:(\d+)##/$data{email_mode} eq $1 ? "checked" : ""/eg;
    $htmlstr =~ s/##com_type##/$com_type/g;
    $htmlstr =~ s/<!-- errmsg_begin -->/$errmsg ? "" : "<!--"/e;
    $htmlstr =~ s/<!-- errmsg_end -->/$errmsg ? "" : "-->"/e;
    $htmlstr =~ s/##errmsg##/$errmsg/g;
    $htmlstr =~ s/##([^#]+)##/$data{$1}/g;

    my $com_mod = $FORM{msgno} ? "修正" : "投稿";
    print _header("$com_modフォーム");
    print $htmlstr;
    print _footer();
    exit;

}

sub com_cancel {

    ($FORM{sid}) = $FORM{sid} =~ /^(\w+)$/;
    unlink("temp/$FORM{sid}") if -e "temp/$FORM{sid}";
    tempfile_clean(); # 一定時間経過した一時ファイルを削除

    print "Location: $CONF{script_name}?", join("&", map { "$_=".uri_escape($FORM{$_}) } grep { $FORM{$_} ne "" } qw(p t o str cond tno)), "\n\n";
    exit;

}

sub com_confirm {

    my %data;
    unless ($FORM{sid}) {
        $FORM{sid} = gen_sid();
        %data = %FORM;
    } else {
        %data = session_data("get", $FORM{sid});
        $FORM{pno} = $data{pno};
    }
    session_data("set", $FORM{sid}, \%FORM);
    my @msg = com_input_check();
    com(\@msg) if @msg;

    # cookie-IDチェック
    $FORM{cid} = cid_required() if $CONF{opt_cid};

    my $com_type;
    if ($FORM{pno}) {
        my $p = table_select("tboard_message.cgi","msgno=$FORM{pno}");
        $p->{msgno} or error("該当する発言データがありませんでした。");
        $com_type = qq{No.$p->{msgno}「$p->{subject}」(投稿者：$p->{name})}.
         qq{への返信};
    } elsif ($FORM{msgno}) {
        $com_type = qq{投稿済み記事の修正};
    } else {
        $com_type = qq{新規投稿};
    }


    my $com_mod = $FORM{msgno} ? "修正" : "投稿";
    print _header("$com_mod内容の確認");
    print "<span style=line-height:180%><br>◆$com_type</span>";
    print mk_shousai_html();
    print <<HTML;
<br>以上の内容でよろしければ「$com_modする」ボタンを押してください。<p>

<input type=hidden name=sid value="$FORM{sid}">
<input type=hidden name=msgno value="$FORM{msgno}">
<input type=submit name=com_done value="$com_modする" style=background-color:$CONF{body_bgcolor};border:solid;border-width:1px;border-color:$CONF{body_text};>
<input type=submit name=com value="戻って再編集する" style=background-color:$CONF{body_bgcolor};border:solid;border-width:1px;border-color:$CONF{body_text};>
<input type=button value="$com_mod中止" style=background-color:$CONF{body_bgcolor};border:solid;border-width:1px;border-color:$CONF{body_text}; onclick="if(confirm('編集途中のデータを破棄して$com_modを中止しますか?')){location.href='$CONF{script_name}?com_cancel&sid=$FORM{sid}'}">
HTML
    print _footer();
    exit;

}

sub com_done {

#    session_data("set", $FORM{sid}, \%FORM);
    my @msg = com_input_check();
    com(\@msg) if @msg;

    # セッションデータのロード
    %FORM = (%FORM, session_data("get", $FORM{sid}));

    # cookie-IDチェック
    $FORM{cid} = cid_required() if $CONF{opt_cid};

    $LOCKED = file_lock();

    $FORM{remote_host} ||= remote_host();
    $FORM{user_agent} ||= $ENV{HTTP_USER_AGENT};

    ### $msgnoの値があるときは修正
    my $msgno = $FORM{msgno};
    my $notify;
    if ($msgno) {
        my $p = table_select("tboard_message.cgi","msgno=$msgno");
        $p->{msgno}
         or error("指定された投稿記事番号はありません。: msgno=$msgno");
        foreach my $key(qw(tno pno indent stat reg_date userid)) {
            $FORM{$key} = $p->{$key}
        }
#        error(map {"$_=>$FORM{$_}"} qw(tno pno indent stat reg_date userid));
        table_update("$FORM{msgno}.cgi",\%FORM,"msgno=$FORM{msgno}","data/message");
        table_update("$FORM{tno}.cgi",\%FORM,"msgno=$FORM{msgno}","data/tree");
        table_update("tboard_message.cgi",\%FORM,"msgno=$FORM{msgno}");
    } else {
        $FORM{msgno} ||= get_new_msgno();
        if ($FORM{pno}) {
            my $p = table_select("tboard_message.cgi","msgno=$FORM{pno}");
            error("該当する返信元記事データ(msgno=$FORM{pno})がありません。")
             unless $p->{msgno};
            $notify = $p if $p->{notify};
            $FORM{indent} = $p->{indent} + 1;
            $FORM{tno} = $p->{tno};
            $FORM{parent_message_color} = $p->{message_color};
            my $t = table_select("tboard_tree.cgi","tno=$p->{tno}");
            $t->{message_cnt}++;
            table_update("tboard_tree.cgi",{message_cnt=>$t->{message_cnt}},"tno=$p->{tno}");
        } else {
            table_insert("tboard_tree.cgi",{tno=>$FORM{msgno},message_cnt=>1},"tno");
        }
        $FORM{tno} ||= $FORM{msgno};
        $FORM{pno} ||= $FORM{msgno};
        $FORM{indent} ||= 0;
        $FORM{stat} = 1;

        table_insert("$FORM{msgno}.cgi",\%FORM,"msgno","data/message");
        table_insert("$FORM{tno}.cgi",\%FORM,"msgno","data/tree");
        table_insert("tboard_message.cgi",\%FORM,"msgno");

    }

    ($FORM{sid}) = $FORM{sid} =~ /^(\w+)$/;
    unlink("temp/$FORM{sid}") if -e "temp/$FORM{sid}";
    tempfile_clean(); # 一定時間経過した一時ファイルを削除

    if (!$msgno and $notify) {
        my $mailstr = <<STR;
No.$notify->{msgno}「$notify->{subject}」(投稿者：$notify->{name})
の投稿に対して以下の返信が付きましたので通知します。

No.$FORM{msgno}「$FORM{subject}」(投稿者：$FORM{name})
$CONF{script_url}?view2=$FORM{msgno}

---------------------
$CONF{prod_name} v$CONF{version}
$CONF{a_url}
STR
        sendmail($notify->{email},$CONF{k_email},
         qq{$CONF{title} 返信通知},$mailstr);
    }

    set_cookie('TBOARD', 30, cookie_data_encode(@{$CONF{cookie_fields}}));
    print "Location: $CONF{script_name}?", join("&", map { "$_=".uri_escape($FORM{$_}) } grep { $FORM{$_} ne "" } qw(p t o str cond tno)), "\n\n";
    exit;

}

sub com_input_check {

    my %data = session_data("get", $FORM{sid});

    my @msg;
    $data{name} or push(@msg,'投稿者名を入力してください。');
    $data{message} or push(@msg,'本文を入力してください。');
    $data{passwd} or push(@msg,'更新/削除用パスワードを入力してください。');
    my $email_reqiured = $data{email_mode} ? 1 : 0;
    $email_reqiured = 1 if $data{notify};
    my @msg_;
    ($data{email}, @msg_) = email_chk($data{email},required=>$email_reqiured);
    push(@msg, @msg_) if @msg_;
    $data{subject} ||= '(無題)';
    @msg;

}

sub cookie_data_encode {

    return base64_encode(join("\t", map { "$_\x1d$FORM{$_}" } @_));

}

sub cookie_data_decode {

    $_[0] .= "=" x (4 - (length($_[0]) % 4)) if length($_[0]) % 4;
    return map { split(/\x1d/,$_,2) } split(/\t/, base64_decode($_[0]));

}

sub cookie_mod {

    my %data = cookie_data_decode(get_cookie('TBOARD'));
    # cookie-IDチェック
    $data{cid} = cid_required() if $CONF{opt_cid};

    $data{email_mode} = 1 if $data{email_mode} eq '';
    $data{disp_type_default} ||= "tree";

    my %str = get_comform_str(%data);

    my $htmlstr = _cookie_mod_html();
    foreach my $f(qw(page_disp_tree page_disp_thread page_disp_list
     page_disp_list2 page_disp_topic)) {
        $htmlstr =~ s/##$f:([^#]+)##/$1 eq $data{$f} ? "selected" : ""/eg;
    }
    foreach my $f(qw(email_mode disp_type_default notify do_link pre)) {
        $htmlstr =~ s/##$f:([^#]+)##/$1 eq $data{$f} ? "checked" : ""/eg;
    }
    foreach (qw(age sex pref email_mode notify url solved solved_str
     message2 icon)) {
        unless ($CONF{"opt_$_"}) {
            $htmlstr =~ s/<!-- opt_${_}_begin -->/<!--/ig;
            $htmlstr =~ s/<!-- opt_${_}_end -->/-->/ig;
        }
    }
    foreach (qw(sex pref age subject_color message_color icon)) {
        $htmlstr =~ s/##${_}list##/$str{$_}/g;
    }
    foreach (qw(body_text body_bgcolor body_link)) {
        $htmlstr =~ s/##$_##/$CONF{$_}/g;
    }
    $htmlstr =~ s/##([^#]+)##/html_output_escape($data{$1})/eg;

    print _header("個人設定");
    print $htmlstr;
    print _footer();
    exit;

}

sub cookie_mod_done {

    set_cookie("TBOARD", 30, cookie_data_encode(@{$CONF{cookie_fields}}));
    print "Location: $CONF{script_name}?", join("&", map { "$_=".uri_escape($FORM{$_}) } grep { $FORM{$_} ne "" } qw(p t o str cond tno)), "\n\n";
    exit;

}

sub crypt_passwd {

    my $passwd = shift;
    my $salt;
    my @salt = ('0'..'9','A'..'Z','a'..'z','.','/');
    foreach (1..8) { $salt .= $salt[rand(@salt)] };
    crypt($passwd,
     index(crypt('a', '$1$a$'), '$1$a$') == 0 ? '$1$'.$salt.'$' : $salt);

}

sub crypt_passwd_is_valid {

    my($plain_passwd, $crypt_passwd) = @_;
    return 0 if $plain_passwd eq '' or $crypt_passwd eq '';
    return crypt($plain_passwd, $crypt_passwd) eq $crypt_passwd ? 1 : 0;

}

sub date_f {

     my($t) = @_;
     my($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($t);
     sprintf("%4d/%02d/%02d(%s) %02d:%02d:%02d", $year + 1900, $mon + 1,
      $mday, (qw(Sun Mon Tue Wed Thu Fri Sat))[$wday], $hour, $min, $sec);

}

sub date_fl {

     my($t) = @_;
     my($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($t);
     sprintf("%02d/%02d/%02d %02d:%02d:%02d", $year - 100, $mon + 1,
      $mday, $hour, $min, $sec);

}


sub decoding {

    my($q) = @_;
    my %FORM;

    if ($q) {
        foreach my $name($q->param()) {
            foreach my $each($q->param($name)) {
#                jcode::convert(\$each,'sjis');
                if (defined($FORM{$name})) {
                    $FORM{$name} = join('|||', $FORM{$name}, $each);
                } else {
                    $FORM{$name} = $each;
                }
            }
        }
        if (keys %FORM == 1 and $FORM{keywords}) {
            $FORM{$FORM{keywords}} = 1;
            delete $FORM{keywords};
        } else {
            foreach my $key(qw(admin cancel chpasswd com display display_img
             init logout menu setup template_update template_update_undo
             wnew)) {
                $FORM{$key} = 1 if exists $FORM{$key} and $FORM{$key} eq '';
            }
        }
    } else {
        my $buf;
        if ($ENV{REQUEST_METHOD} eq "POST") {
            read(STDIN, $buf, $ENV{CONTENT_LENGTH});
        } else {
            $buf = $ENV{QUERY_STRING};
        }
        foreach (split(/&/,$buf)) {
            if (!/=/) { $_ .= "=1"; }
            my($name, $value) = split(/=/);
            $value =~ tr/+/ /;
            $name  =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
            $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
            $value =~ s/\r//g;
#            jcode::convert(\$value, 'sjis');

            if (defined($FORM{$name})) {
                $FORM{$name} = join('|||', $FORM{$name}, $value);
            } else {
                $FORM{$name} = $value;
            }
        }

    }

    %FORM;
}

sub del {


    print "Location: $CONF{script_name}?p=$FORM{p}\n\n";
    exit;

}


sub del_confirm {

    $FORM{msgno} or error("投稿番号が指定されていません。");
    $FORM{passwd} or error("削除用パスワードを入力してください。");
 
    my $p = table_select("tboard_message.cgi","msgno=$FORM{msgno}");
    $p->{msgno} or error("該当する投稿データ(msgno=$FORM{msgno})は存在しませんでした。");
    if ($p->{passwd} ne $FORM{passwd}) {
        error('パスワードが違います。');
    }

    ### 表示は未実装
    my $format;
    $format =~ s/##([^#]+)##/$p->{$1}/g;

    print _header("投稿データの削除");
    print <<HTML;
以下の投稿データを削除してよい場合は「削除」ボタンを押してください。<p>

<form>
$format<hr noshade size=4>
</form>
<form method=post action="$CONF{script_name}">
<input type=hidden name=del value=1>
<input type=hidden name=p value=$FORM{p}>
<input type=hidden name=msgno value="$FORM{msgno}">
<input type=hidden name=passwd value="$FORM{passwd}">
<input type=submit value=削除する>
<input type=button value=戻　る onclick=history.back()>
HTML
    print _footer();
    exit;

}

sub del_tree {

    my @tree = table_select("tboard_tree.cgi","",
     ($CONF{del_tree_method}==2 ? "reg_date::desc" : "last_update::desc"));

    if (@tree > $CONF{tree_max}) {
        foreach (@tree[$CONF{tree_max}..$#tree]) {
            table_delete("tboard_message.cgi","tno=$_->{tno}");
            table_delete("tboard_tree.cgi","tno=$_->{tno}");
        }
    }

}

sub email_chk {

    my($email, %opt) = @_;
    $opt{str} ||= "メールアドレス";
    my @msg;

    if ($opt{required}) {
        $email or push(@msg, $opt{str}.'を入力してください。');
    }
    if ($email =~ /[\0-,\/\:\;<-?\[-\^\`\{-\~]/) {
        push(@msg, $opt{str}.'に特殊文字は使用できません。');
    }
    if ($email =~ /[^ -\~]/) {
        push(@msg, $opt{str}.'に全角文字は使用できません。');
    }
    if ($email && $email !~ /^[-_.!*a-zA-Z0-9\/&+%\#]+\@[-_.a-zA-Z0-9]+\.(?:[a-zA-Z]{2,3})$/) {
        push(@msg, $opt{str}.'が正しくありません。');
    }

    return wantarray ? (lc($email), @msg) : lc($email);

}

sub enc_b64 {

    my($subject) = @_;
    my($str, $padding);
    while ($subject =~ /(.{1,45})/gs) {
        $str .= substr(pack('u', $1), 1);
        chop($str);
    }
    $str =~ tr|` -_|AA-Za-z0-9+/|;
    $padding = (3 - length($subject) % 3) % 3;
    $str =~ s/.{$padding}$/'=' x $padding/e if $padding;
    "=?ISO-2022-JP?B?$str?=";

}

sub error {

    print _header("エラー");
    print "<ul>";
    print map { "<li>$_\n" } @_;
    print "</ul>\n";
    print _footer();
    exit;

}

sub file_lock {

    open(LOCK, "data/lockfile")
     or error("ロック用ファイルが開けませんでした。: $!");
    flock(LOCK, 2);
    1;

}

sub file_save {

    my %extlist = map { $_ => 1 } qw(jpg gif jpeg png);
    my($stream, $filepath, $filename, @extra_extlist) = @_;
    %extlist = map { $_ => 1 } @extra_extlist if @extra_extlist;
    $stream or return;

    $filename =~ s#.*[\\/]([^\\/]+)$#$1# if $filename =~ m#[^\\/]#;
    my($ext) = $filename =~ /\.([^\.]+)$/;
    unless ($extlist{lc($ext)}) {
        error("アップロードできるファイルは、".
         join(" ", sort keys %extlist).
         " の拡張子を持つものに限られています。: $filename");
    }
    open(W, "> $filepath/$filename")
     or error("$filepath/$filename の書き込みに失敗しました。: $!");
    print W $stream;
    close(W);

}

sub gen_sid {

    my @char = (0..9, 'a'..'z', 'A'..'Z');
    while (1) {
        my $sid = join("", map { $char[rand(@char)] } 1..24);
        return $sid unless -e "temp/$sid";
    }

}

sub get_comform_str {

    my %data = @_;
    my %str;
    my @color = split(/\s+/, $CONF{color});
    my @admin_color = get_cookie('TBOARD_ADMIN') ? split(/\s+/, $CONF{admin_color}) : ();
    foreach my $f(qw(sex pref age)) {
        foreach (split(/\s+/, $CONF{"${f}str"})) {
            if ($f eq 'age' and !/\D/) { $_ .= '才'; }
            my $selected = $_ eq $data{$f} ? "selected" : "";
            $str{$f} .= qq{<option value=$_ $selected>$_\n};
        }
    }
    my $i = 0;
    $data{subject_color} ||= $color[0];
    $data{message_color} ||= $color[0];
    foreach (@color, @admin_color) {
        my $checked = $_ eq $data{subject_color} ? "checked" : "";
        $str{subject_color} .= qq{<input type=radio name=subject_color value=$_ $checked><font color="$_">■</font>\n};
        $checked = $_ eq $data{message_color} ? "checked" : "";
        $str{message_color} .= qq{<input type=radio name=message_color value=$_ $checked><font color="$_">■</font>\n};
        if ($i == $#color and get_cookie('TBOARD_ADMIN') and @admin_color) {
            $str{subject_color} .= q{　 [管理者専用色：};
            $str{message_color} .= q{　 [管理者専用色：};
        }
        $i++;
    }
    if (get_cookie('TBOARD_ADMIN') and @admin_color) {
        $str{subject_color} .= q{ ]};
        $str{message_color} .= q{ ]};
    }
    my @icon_list = split(/\n/, $CONF{icon_list});
    my @icon_list_str = split(/\n/, $CONF{icon_list_str});
    foreach my $i(0..$#icon_list) {
        my $selected = $data{icon} eq $icon_list[$i] ? "selected" : "";
        $str{icon} .= qq{<option value="$icon_list[$i]" $selected>$icon_list_str[$i]\n};
    }

    %str;

}

sub get_cookie {

    my($cookie_name) = @_;
    my $cookie_data;
    error('クッキー名を指定してください。') if !$cookie_name;
    foreach (split(/; /, $ENV{HTTP_COOKIE})) {
        my($name, $value) = split(/=/);
        if ($name eq $cookie_name) {
            $cookie_data = $value;
            last;
        }
    }
    wantarray
     ? split(/\!\!\!/, $cookie_data) : (split(/\!\!\!/, $cookie_data))[0];

}


sub get_datetime {

    my $time = shift;
    my($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime($time);
    sprintf("%4d-%02d-%02d %02d:%02d:%02d", $year+1900,++$mon,$mday,
     $hour,$min,$sec);

}

sub get_datetime_for_cookie {

    my($time, $mode) = @_;
    ($time, my $unit) = split(/\s+/, $time, 2);
    $unit = $unit =~ /days?/i ? 86400 : 1;
    my($sec,$min,$hour,$mday,$mon,$year,$wday)
     = $mode eq 'sendmail' ? localtime(time) : gmtime(time + $time * $unit);
    sprintf(('sendmail' ? "%s, %02d %s %04d %02d:%02d:%02d +0900"
     : "%s, %02d-%s-%04d %02d:%02d:%02d GMT"),
     (qw(Sun Mon Tue Wed Thu Fri Sat))[$wday],
     $mday, (qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec))[++$mon],
     $year+1900, $hour, $min, $sec);

}

sub get_datetime_for_sendmail {

    return get_datetime_for_cookie(0, "sendmail");

}

sub get_hour_diff {

    eval { use Time::Local; };
    error("Time::Localモジュールがロードできません。: $@") if $@;
    my $date = shift;
    my($year,$mon,$day,$hour,$min,$sec) = split(/\D+/, $date);
    my $time = timelocal($sec,$min,$hour,$day,$mon-1,$year-1900);
    $get_hour_diff::time ||= time;
#    error($date, $get_hour_diff::time , $time);
    return int(($get_hour_diff::time - $time) / 3600);

}

sub get_new_msgno {

    $LOCKED = file_lock() unless $LOCKED;
    open(R, "data/tboard_msgno.cgi")
     or error("投稿番号データファイルが開けませんでした。: $!");
    my $msgno = <R>;
    open(W, ">data/tboard_msgno.cgi")
     or error("投稿番号データファイルへ書き込みできませんでした。: $!");
    print W ++$msgno;
    close(W);
    return $msgno;

}

sub html_output_escape {

    my $str = shift;
    $str =~ s/&/&amp;/g;
    $str =~ s/>/&gt;/g;
    $str =~ s/</&lt;/g;
    $str =~ s/"/&quot;/g;
    $str =~ s/'/&#39;/g;
    $str;

}

sub init_passwd_file {

    my $file = shift;
    $file ||= "./tboard_passwd.cgi";

    unless (-e $file) {
        open(W, "> $file")
         or error("パスワードファイル($file)の作成に失敗しました。$CONF{message_permission}");
        print W crypt_passwd("12345");
        close(W);
    }
    set_cookie("TBOARD_ADMIN", "", "login");

}

sub init_setup {

    ### tboard_conf.pl が存在しない場合、初回起動と見なす。
    ### パスワード設定フォームに誘導する。

#    %CONF = (%CONF, set_default(\%CONF));
#    %CONF = (%CONF, set_default_init(\%CONF));
    set_default(\%CONF);
    set_default_init(\%CONF);
    write_conf(\%CONF);
    require './tboard_conf.pl';
    %CONF = (%CONF, conf());

    ### データ用ディレクトリ(data)の作成
    ### ツリーデータ用ディレクトリ(data/tree)の作成
    ### 投稿データ用ディレクトリ(data/messages)の作成
    ### 投稿データ過去ログ用ディレクトリ(data/messages.old)の作成
    unless (-d "data") {
        mkdir("data", 0777)
         or error("データ用ディレクトリ(data)の作成に失敗しました。$CONF{message_permission}");
    }
    my %mkdir = (
        tree => "ツリーデータ用ディレクトリ",
        messages => "投稿データ用ディレクトリ",
        "messages.old" => "投稿データ過去ログ用ディレクトリ",
    );
    foreach my $dir(keys %mkdir) {
        unless (-d "data/$dir") {
            mkdir("data/$dir", 0777)
             or error("$mkdir{$dir}(data/$dir)の作成に失敗しました。$CONF{message_permission}うまく行かない場合は、手動でdata/$dirディレクトリを作成してください。");
        }
    }

    ### ロック用ファイル(lockfile)の作成
    ### スレッドマスタファイル(tboard_tree.cgi)の作成
    ### 投稿データファイル(tboard_message.cgi)の作成
    ### 発言番号管理ファイル(tboard_cnt.dat)の作成
    ### 管理用パスワードファイル(tboard_passwd.dat)の作成
    my %mkfile = (
        lockfile => "ロック用ファイル",
        "tboard_tree.cgi" => "スレッドマスタファイル",
        "tboard_message.cgi" => "投稿データファイル",
        "tboard_msgno.cgi" => "発言番号管理ファイル",
        "tboard_passwd.cgi" => "管理用パスワードファイル",
    );
    foreach my $file(keys %mkfile) {
        unless (-e "data/$file") {
            open(W, "> data/$file")
             or error("$mkfile{$file}(data/$file)の作成に失敗しました。$CONF{message_permission}");
            close(W);
        }
    }

}

sub login {

    open(R, "tboard_passwd.cgi")
     or error("パスワードファイルが開けませんでした。: $!");
    chomp(my $login_passwd = <R>);
    close(R);
    unless (crypt_passwd_is_valid($FORM{passwd}, $login_passwd)) {
        error('管理用パスワードが違います。',"$FORM{passwd}, $login_passwd");
    }
    set_cookie('TBOARD_ADMIN', "", "login");
    if ($FORM{do_cache}) {
        set_cookie('TBOARD_ADMIN_CACHE', 30, $FORM{passwd});
    }
    print "Location: $CONF{script_name}?admin\n\n";
    exit;

}

sub login_check {

    init_passwd_file("tboard_passwd.cgi") unless -e "tboard_passwd.cgi";
    login_form() unless get_cookie('TBOARD_ADMIN');

}

sub login_form {

    my $passwd_cache = get_cookie('TBOARD_ADMIN_CACHE');
    my $checked = $passwd_cache ne '' ? 'checked' : "";
    print _admin_header();
    print <<HTML;
このシステムを利用するにはログインが必要です。<br>
管理用パスワードを入力してください。<p>

<form action=$CONF{script_name} method=post>
<input type=hidden name=login value=1>
<input type=password name=passwd size=14 value="$passwd_cache">
<input type=submit value=ログイン><br>
<input type=checkbox name=do_cache value=1 $checked>パスワードを記憶する
</form><p>
HTML
    print _footer();
    exit;

}

sub logout {

    set_cookie('TBOARD_ADMIN');
    print _admin_header();
    print <<HTML;
ログアウトしました。<p><br><br><br>
<a href="$CONF{script_name}?admin">管理用メニューへ</a><p>
HTML
    print _footer();

    exit;

}

sub mailform {

    my $msgno = $FORM{mailform};

    # クッキーデータをロード
    my %data = cookie_data_decode(get_cookie('TBOARD'));

    my $p = table_select("tboard_message.cgi","msgno=$msgno,stat=1");
    $p->{msgno} or error("該当する投稿データ(msgno=$msgno)がありませんでした");
    error("この投稿(msgno=$msgno)の投稿者に対してメールの転送はできません。")
     unless $p->{email_mode} == 2;

    my $htmlstr = _mailform_html();
    $htmlstr =~ s/##msgno##/$msgno/g;
    $htmlstr =~ s/##subject##/$p->{subject}/g;
    $htmlstr =~ s/##name##/$p->{name}/g;
    $htmlstr =~ s/##body_text##/$CONF{body_text}/g;
    $htmlstr =~ s/##body_bgcolor##/$CONF{body_bgcolor}/g;
    $htmlstr =~ s/##script_name##/$CONF{script_name}/g;
    $htmlstr =~ s/##([^#]+)##/$data{$1}/g;

    print _header("メール送信フォーム");
    print $htmlstr;
    print _footer();
    exit;

}

sub mailform_done {

    my $msgno = $FORM{msgno};

    my $p = table_select("tboard_message.cgi","msgno=$msgno,stat=1");
    $p->{msgno} or error("該当する投稿データ(msgno=$msgno)がありませんでした");
    error("この投稿(msgno=$msgno)の投稿者に対してメールの転送はできません。")
     unless $p->{email_mode} == 2;

    my @msg = mailform_input_check(\%FORM);
    error(@msg) if @msg;

    jcode::convert(\$FORM{name}, 'jis', 'euc');
    my $from = '"' . enc_b64($FORM{name}) . '" <' . $FORM{email} . '>';
    my $mailstr = <<STR;
※「$CONF{title}($CONF{script_url})」
  No.$msgno「$p->{subject}」に対する転送メールです。
--------------------------------------------------------------------
$FORM{message}
---------------------
$CONF{prod_name} v$CONF{version}
$CONF{a_url}
STR

    sendmail($p->{email}, $from, $FORM{subject}, $mailstr);

    print _header("メール送信フォーム");
    print "<p>送信しました。<p><a href=$CONF{script_name}?>投稿一覧へ</a>";
    print _footer();
    exit;

}

sub mailform_input_check {

    my @msg;
    my $data_ref = shift;
    $data_ref->{name} or push(@msg,'投稿者名を入力してください。');
    $data_ref->{message} or push(@msg,'本文を入力してください。');
    my @msg_;
    ($data_ref->{email}, @msg_) = email_chk($data_ref->{email},required=>1);
    push(@msg, @msg_) if @msg_;
    $data_ref->{subject} ||= '(無題)';
    @msg;

}

sub mk_list {

    my($d, $mode) = @_;
    my $htmlstr = $mode eq 'topic' ? $CONF{topic_format} : $CONF{list_format};

    $d->{subject_} = $d->{subject};
    $d->{subject_} = truncate_str($d->{subject}, $CONF{subject_length})
     if $CONF{subject_length} and length($d->{subject}) > $CONF{subject_length};
    $d->{subject} = html_output_escape($d->{subject});
    $d->{age} = "/$d->{age}" if $d->{age};
    $d->{pref} = "/$d->{pref}" if $d->{pref};
    $d->{sex} = "/$d->{sex}" if $d->{sex};
    foreach (qw(body_text body_bgcolor)) {
        $htmlstr =~ s/##$_##/$CONF{$_}/eg;
    }
    $htmlstr =~ s/##subject##/<a href="$CONF{script_name}?view2=$d->{msgno}&p=$FORM{p}&o=$FORM{o}" title="$d->{subject}"><font color="$d->{subject_color}">$d->{subject_}<\/font><\/a>/g;
    $htmlstr =~ s/##new##/($CONF{new_mark} and $CONF{new_mark} > get_hour_diff($d->{reg_date})) ? $CONF{new_mark_str} : ""/eg;
    $htmlstr =~ s/##up##/($d->{reg_date} ne $d->{last_update} and $CONF{new_mark} > get_hour_diff($d->{last_update})) ? $CONF{up_mark_str} : ""/eg;
    $htmlstr =~ s/##([^#]+)##/$d->{$1}/g;
    $htmlstr;

}

sub mk_navi_bar {

    my($hl, %d) = @_;
    my %button = (
        1 => { url=>$CONF{home_url}, str=>"ＨＯＭＥ"},
        2 => { url=>"$CONF{script_name}?com&p=$d{p}&o=$d{o}", str=>"新規投稿"},
        3 => { url=>"$CONF{script_name}?help", str=>"ＨＥＬＰ" },
        4 => { url=>"$CONF{script_name}?", str=>"ツリー表示" },
        5 => { url=>"$CONF{script_name}?t=thread", str=>"スレッド表示" },
        6 => { url=>"$CONF{script_name}?t=list", str=>"タイトルのみ" },
        7 => { url=>"$CONF{script_name}?t=list2", str=>"全表示" },
        8 => { url=>"$CONF{script_name}?t=topic", str=>"トピック表示" },
        9 => { url=>"$CONF{script_name}?search_form&p=$d{p}&o=$d{o}",
         str=>"検　索" },
        10 => { url=>"$CONF{script_name}?cookie_mod", str=>"個人設定" },
        99 => { url=>"$CONF{script_name}?admin", str=>"管理用" },
        tree   => 4,
        thread => 5,
        list   => 6,
        list2  => 7,
        topic  => 8,
    );

    $hl = $button{$hl} if $hl =~ /\D/;

    my $width = int(700 / scalar(grep(/^\d+$/, keys %button)));
    my $str = <<STR;
<table border=0 cellpadding=0 cellspacing=0 width=700 bgcolor="$CONF{body_text}">
<tr><td><table border=0 cellpadding=2 cellspacing=1 width=100%>
<tr>
STR
    foreach my $i(sort { $a <=> $b } grep(/^\d+$/, keys %button)) {
        my $hl_bgcolor = $i == $hl ? $CONF{hl_bgcolor} : $CONF{body_bgcolor};
        my $hl_link = $i == $hl ? qq{} : qq{<a href="$button{$i}->{url}">};
        my $hl_link2 = $i == $hl ? qq{</a>} : qq{};
        $str .= <<STR;
<td bgcolor="$hl_bgcolor" align=center><span style=font-size:9.5pt;>$hl_link$button{$i}->{str}$hl_link2</span></td>
STR
    }
    $str .= "</table></td></tr></table>";

    return $str;

}

sub mk_shousai_html {

    my($msgno, $p) = shift;
    my $p2;
    if ($msgno and !exists $FORM{name}) {
        $p ||= table_select("tboard_message.cgi","msgno=$msgno,stat=1");
        $p->{msgno} or error("該当する投稿データ(msgno=$msgno)がありませんでした");
    } else {
        $p = \%FORM;
        $p->{msgno} ||= "*";
        $p->{reg_date} = get_datetime(time);
        $p->{remote_host} = remote_host();
        $p2 = table_select("tboard_message.cgi","msgno=$p->{pno},stat=1");
        $p->{parent_message_color} = $p2->{parent_message_color};
    }
    $p->{cid} = $p->{cid} ? "/ID:$p->{cid}" : "";


    $p->{message} = join("\n", map { (/^\s*> */ and $p->{parent_message_color}) ? "\x{01}font color=$p->{parent_message_color}\x02$_\x{01}/font\x02" : $_ } split(/\n/, $p->{message}));
    $p->{subject_dsp} = html_output_escape($p->{subject});
    $p->{subject_dsp} = qq{<font color="$p->{subject_color}">$p->{subject_dsp}</font>};
    $p->{message_dsp} = html_output_escape($p->{message});
    $p->{message_dsp} =~ s/\x01/</g;
    $p->{message_dsp} =~ s/\x02/>/g;
#error($p->{message_dsp});
    $p->{message_dsp} = "<pre>$p->{message_dsp}</pre>" if $p->{pre};
    $p->{message_dsp} =~ s/\n/<br>\n/g unless $p->{pre};
    $p->{message_dsp} = qq{<font color="$p->{message_color}">$p->{message_dsp}</font>};
    $p->{message2_dsp} = html_output_escape($p->{message2});
    $p->{message2_dsp} =~ s/\n/<br>/g;
    if ($p->{do_link}) {
        $p->{message_dsp} = autolink_email($p->{message_dsp});
        $p->{message_dsp} = autolink_url($p->{message_dsp});
        $p->{message2_dsp} = autolink_email($p->{message2_dsp});
        $p->{message2_dsp} = autolink_url($p->{message2_dsp});
    }
    if ($p->{url} and $p->{url} ne "http://") {
        $p->{url_dsp} = qq|/<a href="$p->{url}" target=_blank><img src=img/home.gif border=0></a>|;
    } else {
        $p->{url_dsp} = "";
    }
    if ($p->{email}) {
        if ($p->{email_mode} == 1) {
            $p->{email_dsp} = qq|/<a href="mailto:$p->{email}"><img src=img/email.gif border=0></a>|;
        } elsif ($p->{email_mode} == 2) {
            $p->{email_dsp} = qq|/<a href="$CONF{script_name}?mailform=$p->{msgno}"><img src=img/email.gif border=0></a>|;
        } else {
            $p->{email_dsp} = "";
        }
    } else {
        $p->{url} = "";
    }
    $p->{age} = "/$p->{age}" if $p->{age};
    $p->{pref} = "/$p->{pref}" if $p->{pref};
    $p->{sex} = "/$p->{sex}" if $p->{sex};

    if ($p->{icon}) {
        $p->{icon_dsp} = qq{<img src="img/icon/$p->{icon}">};
    }

    ### 表示は未実装
    my $format = _view2_html();
    foreach (qw(message message2 subject url email)) {
        $format =~ s/##$_##/$p->{"${_}_dsp"}/eg;
    }
    foreach (qw(body_text body_bgcolor script_name)) {
        $format =~ s/##$_##/$CONF{$_}/eg;
    }
    $format =~ s/##submit_mode##/$msgno ? "submit" : "button"/eg;
    $format =~ s/<!-- moddel_begin -->/$msgno ? "" : "<!--"/eg;
    $format =~ s/<!-- moddel_end -->/$msgno ? "" : "-->"/eg;
    $format =~ s/##([^#]+)##/$p->{$1}/g;

    return $format;

}

sub mk_topic {

    my($ref, $message_cnt) = @_;
    $ref->{message_cnt} = $message_cnt;
    return mk_list($ref, "topic");

}

sub mk_tree {

    my $tno = shift;
    my %pno;
    my %data;
    my %done;
    my %d;

    foreach my $p(table_select("tboard_message.cgi","tno=$tno")) {
        $data{$p->{msgno}} = { %$p };
        $pno{$p->{pno}} .= defined $pno{$p->{pno}} ? ",$p->{msgno}" : $p->{msgno};
    }

    my @liststr;
    foreach my $msgno(sort { $a <=> $b } keys %data) {
        mk_tree_data($msgno,{done=>\%done,pno=>\%pno,data=>\%data,
         liststr=>\@liststr});
    }

    my $liststr;
    my %b;
    foreach my $line(reverse @liststr) {
        my $max;
        my %n;
        unless ($line->[1]) {
            $liststr = "▽" . $line->[2] . "<br>\n" . $liststr;
            next;
        }
        $max = $line->[1];
        $b{$line->[1]} ? ( $n{$line->[1]} = '├' )
                       : ( $n{$line->[1]} = '└' );
        foreach my $i(keys %b) {
            if ($i > $line->[1]) {  next; }
            $max = $i if $max < $i;
            if ($b{$i} and $i != $line->[1]) { $n{$i} = '│' }
        }
        $liststr = "<tt>" .
                   join("", map { $_ or '　' } @n{0..$max}) . "</tt>" .
                   $line->[2] . "<br>\n" . $liststr;
        %b = map { $_, $n{$_} } (1..$line->[1]);
    }

    return $liststr;

}

sub mk_tree_data {

    my($msgno,$ref) = @_;
    return if $ref->{done}->{$msgno};
    $ref->{data}->{$msgno}->{subject}
     = html_output_escape($ref->{data}->{$msgno}->{subject});
    if ($ref->{data}->{$msgno}->{del_flag} == 1) {
        $ref->{data}->{$msgno}->{subject} = "(投稿者削除)";
        $ref->{data}->{$msgno}->{name} = "";
    } elsif ($ref->{data}->{$msgno}->{del_flag} == 2) {
        $ref->{data}->{$msgno}->{subject} = "(管理者削除)";
        $ref->{data}->{$msgno}->{name} = "";
    }
    my $list_format_ = $CONF{tree_format};
    $ref->{data}->{$msgno}->{subject_} = $ref->{data}->{$msgno}->{subject};
    $ref->{data}->{$msgno}->{subject_}
     = truncate_str($ref->{data}->{$msgno}->{subject}, $CONF{subject_length})
     if $CONF{subject_length}
     and length($ref->{data}->{$msgno}->{subject}) > $CONF{subject_length};
    $list_format_ =~ s/##subject##/<a href="$CONF{script_name}?view2=$msgno&p=$FORM{p}&o=$FORM{o}" title="$ref->{data}->{$msgno}->{subject}"><font color="$ref->{data}->{$msgno}->{subject_color}">$ref->{data}->{$msgno}->{subject_}<\/font><\/a>/g;
#    $list_format_ =~ s/##new##/($CONF{new_mark} and $CONF{new_mark} > get_hour_diff($ref->{data}->{$msgno}->{reg_date})) ? get_hour_diff($ref->{data}->{$msgno}->{reg_date}) : ""/eg;
    $list_format_ =~ s/##new##/($CONF{new_mark} and $CONF{new_mark} > get_hour_diff($ref->{data}->{$msgno}->{reg_date})) ? $CONF{new_mark_str} : ""/eg;
    $list_format_ =~ s/##up##/($ref->{data}->{$msgno}->{reg_date} ne $ref->{data}->{$msgno}->{last_update} and $CONF{new_mark} > get_hour_diff($ref->{data}->{$msgno}->{last_update})) ? $CONF{up_mark_str} : ""/eg;
    $list_format_ =~ s/##([^#]+)##/$ref->{data}->{$msgno}->{$1}/g;
    push(@{$ref->{liststr}}, [$msgno,$ref->{data}->{$msgno}->{indent},$list_format_]);
    $ref->{done}->{$msgno} = 1;
    foreach my $child(split(/,/, $ref->{pno}->{$msgno})) { 
        mk_tree_data($child,$ref);
    }

}

sub remote_host {

    if ($ENV{REMOTE_HOST} eq $ENV{REMOTE_ADDR} or $ENV{REMOTE_HOST} eq '') {
        gethostbyaddr(pack('C4',split(/\./,$ENV{REMOTE_ADDR})),2)
         or $ENV{REMOTE_ADDR};
    } else {
        $ENV{REMOTE_HOST};
    }
}

sub sendmail {

    my($mailto, $from, $subject, $mailstr, $date) = @_;

    jcode::convert(\$subject,'jis');
    jcode::convert(\$mailstr,'jis');
    $subject = enc_b64($subject) if $subject =~ /[^\t\n\x20-\x7e]/;
    $date ||= get_datetime_for_sendmail();

    my $maildata = <<STR;
To: $mailto
From: $from
Subject: $subject
Content-Transfer-Encoding: 7bit
Mime-Version: 1.0
Content-Type: text/plain; charset=ISO-2022-JP

$mailstr
STR
    $maildata = "Date: $date\n$maildata" if $date;

    if ($CONF{mailsend} eq 'smtp') {
        unless ($smtp) {
            eval { use Net::SMTP; };
            error("Net::SMTPモジュールが使用できません。: $@") if $@;
            $smtp = Net::SMTP->new($CONF{smtp});
        }
        $smtp->mail($from);
        $smtp->to($mailto);
        $smtp->data();
        $smtp->datasend($maildata);
        $smtp->dataend();
#        $smtp->quit;
    } else {
        open(SEND, "|$CONF{sendmail} -t 1>/dev/null 2>/dev/null")
         or error("$mailto への送信に失敗しました。: $!");
        print SEND $maildata;
        close(SEND) or error("$mailto への送信に失敗しました。: $!");
    }
}

sub session_data {

    my($mode, $sid, $data_ref) = @_;
    ($sid) = $sid =~ /^(\w+)$/;
    $sid or error("session_data: セッションIDを指定してください。");

    if ($mode eq 'set') {
        open(W, "> temp/$sid")
         or error("セッションデータファイルの書き込みができませんでした。: $!");
        foreach my $f(sort @{$CONF{session_data_fields}}) {
            my $v = $data_ref->{$f};
            $v =~ s/\r\n|\r|\n/\x0b/g;
            print W "$f\x1d$v\n";
        }
        close(W);
    } else {
        my %data;
        open(R, "temp/$sid");
        while (<R>) {
            chomp;
            my($f,$v) = split(/\x1d/, $_, 2);
            $v =~ s/\x0b/\n/g;
            $data{$f} = $v;
        }
        close(R);
        return %data;
    }

}

sub set_cid {

    if ($CONF{opt_cid}) {
        my $cid = get_cookie("TBOARD_CID");
        set_cookie("TBOARD_CID", 30, ($cid or gen_sid()));
    }

}

sub set_cookie {

    my($cookie_name, $expire, @cookie_data) = @_;
    my($cookie_data) = join('!!!', @cookie_data);
    $expire = "expires=". get_datetime_for_cookie("$expire days") . "; "
     if $expire;
    print "Set-Cookie: $cookie_name=$cookie_data; $expire\n";

}

sub set_default {

    my $hash_ref = shift;

    $hash_ref->{title}            ||= "$CONF{prod_name} v$CONF{version}";
    $hash_ref->{title_color}      ||= "#333333";
    $hash_ref->{title_font_size}  ||= "18";
    $hash_ref->{title_align}      ||= "left";
    $hash_ref->{tree_max}         ||= 100;
    $hash_ref->{del_tree_method}  ||= 1;

    $hash_ref->{page_disp_tree}   ||= 10;
    $hash_ref->{page_disp_thread} ||= 5;
    $hash_ref->{page_disp_list}   ||= 15;
    $hash_ref->{page_disp_list2}  ||= 10;
    $hash_ref->{page_disp_topic}  ||= 15;

    $hash_ref->{color}        ||= '#333333 steelblue blue navy green darkgreen brown darkorange purple';

    $hash_ref->{sexstr}       ||= '男性 女性 中性 ひみつ';
    $hash_ref->{prefstr}      ||= '職場 自宅 客先 ひみつ 北海道 青森県 岩手県 宮城県 秋田県 山形県 福島県 茨城県 栃木県 群馬県 埼玉県 千葉県 東京都 神奈川県 山梨県 長野県 新潟県 富山県 石川県 福井県 岐阜県 静岡県 愛知県 三重県 滋賀県 京都府 大阪府 兵庫県 奈良県 和歌山県 鳥取県 島根県 岡山県 広島県 山口県 徳島県 香川県 愛媛県 高知県 福岡県 佐賀県 長崎県 熊本県 大分県 宮崎県 鹿児島県 沖縄県 海外';
    $hash_ref->{agestr}        ||= 'こども 少年 少女 若者 青年 乙女 10代 20代 30代 40代 50代 60代以上';

    $hash_ref->{body_text}     ||= '#333333';
    $hash_ref->{body_bgcolor}  ||= '#ffffff';
    $hash_ref->{body_link}     ||= '#ff3333';
    $hash_ref->{body_vlink}    ||= '#ff6666';
    $hash_ref->{body_alink}    ||= '#0000ff';

    $hash_ref->{new_mark}  ||= 0;

    $hash_ref->{mailsend}  ||= 'sendmail';

    %$hash_ref;

}

sub set_default_init {

    my $hash_ref = shift;
    chomp($hash_ref->{stylesheet} = <<'STR');
  body,pre,td,th { font-size: 10.5pt; line-height:120%; }
  a {text-decoration: none;}
  a:hover { color:red; text-decoration:underline; }
STR

    $hash_ref->{admin_color}    ||= 'red';
    $hash_ref->{subject_length} ||= 70;
    $hash_ref->{opt_age}        ||= 0;
    $hash_ref->{opt_sex}        ||= 0;
    $hash_ref->{opt_pref}       ||= 0;
    $hash_ref->{opt_email_mode} ||= 0;
    $hash_ref->{opt_notify}     ||= 0;
    $hash_ref->{opt_url}        ||= 1;
    $hash_ref->{opt_solved}     ||= 0;
    $hash_ref->{opt_solved_str} = '<font color=red>[解決!]</font>';
    $hash_ref->{opt_message2}   ||= 0;
    $hash_ref->{opt_cid}        ||= 1;
    $hash_ref->{opt_icon}       ||= 0;
    $hash_ref->{icon_list}      ||= join("\n", (map { sprintf("a_%04d.gif", $_) } 1..14),(map { sprintf("b_%04d.gif", $_) } 1..14));
    $hash_ref->{icon_list_str}  ||= join("\n", qw{
     わーい(ブルー) わははは(ブルー) わくわく(ブルー) うぇーん(ブルー)
     ちゅっ(ブルー) ぷん(ブルー) ごめんね(ブルー) ありがと(ブルー)
     Zzzz...(ブルー) にやり(ブルー) 冷や汗(ブルー) ごるぁぁ(ブルー)
     らんらん♪(ブルー) ぽっ(ブルー) わーい(ピンク) わははは(ピンク)
     わくわく(ピンク) うぇーん(ピンク) ちゅっ(ピンク) ぷん(ピンク)
     ごめんね(ピンク) ありがと(ピンク) Zzzz...(ピンク) にやり(ピンク)
     冷や汗(ピンク) ごるぁぁ(ピンク) らんらん♪(ピンク) ぽっ(ピンク)
    });
    $hash_ref->{new_mark}       ||= 24;
    $hash_ref->{new_mark_str}   ||= '<img src=img/new.gif alt=NEW! border=0>';
    $hash_ref->{up_mark_str}    ||= '<img src=img/up.gif alt=UP! border=0>';
    $hash_ref->{sendmail}       ||= '/usr/sbin/sendmail';

    %$hash_ref;

}

sub setup {

    my $init = shift;
    $init = "<input type=hidden name=init value=1>" if $init;
    login_check();

    my $htmlstr = _setup_html();

    foreach my $f(qw(subject_length page_disp_tree
     page_disp_thread page_disp_list page_disp_list2 page_disp_topic
     tree_max del_tree_method new_mark)) {
        $htmlstr =~ s/##$f:([^#]+)##/$1 eq $CONF{$f} ? "selected" : ""/eg;
    }
    foreach my $f(qw(title_align title_is_bold opt_age opt_sex opt_pref
     opt_email_mode opt_notify opt_url opt_solved opt_message2 opt_cid
     opt_icon mailsend)) {
        $htmlstr =~ s/##$f:([^#]+)##/$1 eq $CONF{$f} ? "checked" : ""/eg;
    }
    $htmlstr =~ s/##([^#]+)##/html_output_escape($CONF{$1})/eg;

    print _admin_header("環境設定");
    print $htmlstr;
    print _footer();
    exit;
}

sub setup2 {

    login_check();

    %FORM = (%FORM, set_default(\%FORM));

    write_conf(\%FORM);

    if ($FORM{init}) {
        print "Location: $CONF{script_name}?chpasswd\n\n";
    } else {
        print _admin_header();
        print <<HTML;
環境設定を更新しました。<p><br><br>
<a href="$CONF{script_name}?admin">管理用メニューへ</a><p>
HTML
        print _footer();
        exit;
    }

}

sub setver {
#########################################
#### この部分は変更しないでください。####
#########################################
    my %setver = (
        prod_name => q{Tree Board},
        version   => q{0.1},
        signature => q{Author's page},
        a_email   => q{info@psl.ne.jp},
        a_url     => q{http://www.psl.ne.jp/},
    );
    $setver{credit} = qq{<div align=right><font size=2><b><a href="$setver{a_url}" target=_top>$setver{prod_name} v$setver{version}</a></b></font>};

    %setver;

}

sub table_delete {

    my($tablename,$key,$path) = @_;
    $path ||= "data";
    ($path) = $path =~ m#^((?:\.\./|[^/]?)[/\d\w]+)$#;

    my($k,$v) = split(/\s*=\s*/, $key);
    error("照合条件が指定されていません。: $key") unless $k;
    my @data;
    my @deleted;

    $LOCKED = file_lock() unless $LOCKED;
    open(R, "$path/$tablename")
     or error("テーブルデータファイルが開けませんでした。: $!",@_);
    while (my $line = <R>) {
        my %d;
        chomp($line);
        @d{@{$tables{$tablename}}} = split(/\t/, $line);
        if ($d{$k} eq $v) {
            push(@deleted, [@d{@{$tables{$tablename}}}]);
            next;
        }
        push(@data, $line);
    }

    open(W, ">$path/$tablename")
     or error("テーブルデータファイルが開けませんでした。: $!",@_);
    foreach (@data) { print W "$_\n"; }
    close(W);

    return @deleted;

}

sub table_insert {

    my($tablename,$data_ref,$key,$path) = @_; #error($key);
    my $hash_tables_key = $tablename;

    ### tboard.cgi用の拡張部分 ここから ####
    if (($tablename) = $tablename =~ /^(\d+\.cgi)$/) {
        $hash_tables_key = "tboard_message.cgi";
    } else {
        $tablename = $hash_tables_key;
    }
    ### tboard.cgi用の拡張部分 ここまで ####

    $path ||= "data";
    ($path) = $path =~ m#^((?:\.\./|[^/]?)[/\d\w]+)$#;

    unless (-e "$path/$tablename") {
        ($tablename) = $tablename =~ /^(\d+\.cgi)$/;
        $tablename or error("不正なテーブル名を指定しています。: $tablename");
    }

    $LOCKED = file_lock() unless $LOCKED;
    my $serial_max;
    if ($key) {
        open(R, "$path/$tablename");
#         or error("テーブルデータファイルが開けませんでした。: $!",@_);
        while (<R>) {
            my %d;
            my $skip;
            chomp;
            @d{@{$tables{$hash_tables_key}}} = split(/\t/);
            if ($data_ref->{$key} eq '__serial__') {
                $serial_max = $d{$key} if $serial_max <= $d{$key};
            } else {
                if ($d{$key} eq $data_ref->{$key}) {
                    error("キーが重複しています。: $key=$d{$key}");
                }
            }
        }
    }
    $data_ref->{$key} = ++$serial_max if $data_ref->{$key} eq '__serial__';
    $data_ref->{reg_date} = $data_ref->{last_update} = get_datetime(time);
    open(W, ">>$path/$tablename")
     or error("テーブルデータファイルが開けませんでした。: $!",@_);
    foreach (@{$tables{$hash_tables_key}}) {
        $data_ref->{$_} =~ s/\r?\n/\x0b/g;
        $data_ref->{$_} =~ s/\t/ /g;
    }
    print W join("\t", join("\t", map { $data_ref->{$_} }
     @{$tables{$hash_tables_key}})), "\n";
    close(W);

    return $serial_max;

}

sub table_select {

    my($tablename,$cond,$order,$path) = @_;
    my $real_tablename = $tablename;

    ### tboard.cgi用の拡張部分 ここから ####
    if ($tablename eq 'tboard_message.cgi') {
        if ($cond =~ /msgno=(\d+)/) {
            ($real_tablename, $path) = ("$1.cgi", "data/message");
        } elsif ($cond =~ /tno=(\d+)/) {
            ($real_tablename, $path) = ("$1.cgi", "data/tree");
        }
    }
    ### tboard.cgi用の拡張部分 ここまで ####

    $path ||= "data";
    ($path) = $path =~ m#^((?:\.\./|[^/]?)[/\d\w]+)$#;

    my %cond;
    my %op;
    my @row;
    my @row2;
    my $order_array_ref;
    my $cnt = 0;
    my $test;

    my %str_op = (
        q{<=} => q{le},
        q{>=} => q{ge},
        q{<}  => q{lt},
        q{>}  => q{gt},
        q{=}  => q{eq},
        q{!=} => q{ne},
        q{=~} => q{=~}
    );
    my $cond_sub = {
        q{<=} => sub { return $_[0] <= $_[1] },
        q{le} => sub { return $_[0] le $_[1] },
        q{>=} => sub { return $_[0] >= $_[1] },
        q{ge} => sub { return $_[0] ge $_[1] },
        q{>}  => sub { return $_[0] >  $_[1] },
        q{gt} => sub { return $_[0] gt $_[1] },
        q{<}  => sub { return $_[0] <  $_[1] },
        q{lt} => sub { return $_[0] lt $_[1] },
        q{=}  => sub { return $_[0] =  $_[1] },
        q{eq} => sub { return $_[0] eq $_[1] },
        q{!=} => sub { return $_[0] != $_[1] },
        q{ne} => sub { return $_[0] ne $_[1] },
        q{=~} => sub { return $_[0] =~ /$_[1]/ },
    };

    my $cond_op;
    if ($cond =~ /^OR:(.*)$/i) {
        $cond = $1;
        $cond_op = "OR";
    }
    foreach my $cond0(split(/\s*,\s*/,$cond)) {
        my($f,$op,$v,$num) = $cond0 =~ /^([^<>=~]+)\s*(<=|>=|\!=|=\~|>|<|=)\s*(.+)(\:num)?$/;
        next unless $f;
        if (exists $cond{$f}) {
            $cond{$f} = join("\0", $cond{$f}, $v);
            $op{$f} = join("\0", $op{$f}, ($num ? $op : $str_op{$op}));
        } else {
            $cond{$f} = $v;
            $op{$f} = $num ? $op : $str_op{$op};
        }
    }

    $LOCKED = file_lock() unless $LOCKED;
    open(R, "$path/$real_tablename")
     or error("table_select: テーブルデータファイルが開けませんでした。: $!",@_);
    while (<R>) {
        my %d;
        my %hit;
        chomp;
        @d{@{$tables{$tablename}}} = split(/\t/);
        foreach (@d{@{$tables{$tablename}}}) { s/\x0b/\n/g };
        foreach my $cond(keys %cond) {
            $test .= "$d{$cond} $op{$cond} $cond{$cond}\n";
            my @cond = split(/\0/, $cond{$cond});
            my @op = split(/\0/, $op{$cond});
            my $hit;
            foreach my $i(0..$#cond) {
                if (&{$cond_sub->{$op[$i]}}($d{$cond},$cond[$i])) {
                    $hit = 1;
                    last;
                }
            }
            $hit{$cond} = 1 if $hit;
        }
        next unless keys %hit == keys %cond;
        push(@row, {%d});
    }
    close(R);

    if ($order) {
        my @sortstr;
        foreach my $o(split(/\s*,\s*/, $order)) {
            my($f,$t,$desc) = split(/:/, $o);
            ($f) = $f =~ /^(\w+)$/;
            my $op = $t eq 'num' ? "<=>" : "cmp";
            if ($desc =~ /\[(.*)\]/) {
                my %order;
                my $c = 0;
                foreach my $k(split(/\s*;\s*/, $1)) {
                    $order{$k} = $c++;
                }
                $order_array_ref = { %order };
            }

            my($a_,$b_) = $desc =~ /\[/
                         ? ("\$order_array_ref->{\$a->{$f}}",
                            "\$order_array_ref->{\$b->{$f}}")
                         : ($desc eq 'desc'
                            ? ("\$b->{$f}","\$a->{$f}")
                            : ("\$a->{$f}","\$b->{$f}")
                           );
            push(@sortstr, "$a_ $op $b_");
        }
        my $evalstr = "sort { ". join(" or ", @sortstr) . " } \@row;";
        @row = eval $evalstr;
        error($@,$evalstr) if $@;
    }
    return (wantarray ? @row : $row[0]);

}
sub table_update {

    my($tablename,$data_ref,$key,$path) = @_;
    my $hash_tables_key = $tablename;

    ### tboard.cgi用の拡張部分 ここから ####
    if (($tablename) = $tablename =~ /^(\d+\.cgi)$/) {
        $hash_tables_key = "tboard_message.cgi";
    } else {
        $tablename = $hash_tables_key;
    }
    ### tboard.cgi用の拡張部分 ここまで ####


    $path ||= "data";
    ($path) = $path =~ m#^((?:\.\./|[^/]?)[/\d\w]+)$#;
    my($k,$v) = split(/\s*=\s*/, $key);
    error("照合条件が指定されていません。: $key") unless $k;

    my @data;
    my @updated;

    $LOCKED = file_lock() unless $LOCKED;
    open(R, "$path/$tablename")
     or error("テーブルデータファイルが開けませんでした。: $!",@_);
    while (my $line = <R>) {
        my %d;
        chomp($line);
        @d{@{$tables{$hash_tables_key}}} = split(/\t/, $line);
        if ($d{$k} eq $v) {
            push(@updated, [@d{@{$tables{$hash_tables_key}}}]);
            $d{last_update} = get_datetime(time);
            foreach (keys %$data_ref) {
                $data_ref->{$_} =~ s/\r?\n/\x0b/g;
                $data_ref->{$_} =~ s/\t/ /g;
                $d{$_} = $data_ref->{$_};
            }
            # キーのあるフィールドのみ上書き
            push(@data, join("\t", @d{@{$tables{$hash_tables_key}}}));
        } else {
            push(@data, $line);
        }
    }

    open(W, ">$path/$tablename")
     or error("テーブルデータファイルが開けませんでした。: $!",@_);
    foreach (@data) { print W "$_\n"; }
    close(W);

    return @updated;

}

sub tempfile_clean {

    my $time = time;
    ### 投稿一時データファイルの削除
    opendir(DIR, "temp") or error("tempディレクトリが開けませんでした。: $!");
    foreach my $file(grep(/^\w+$/, readdir(DIR))) {
        ($file) = $file =~ /^(\w+)$/;
        unlink("temp/$file")
         if $time - (stat("temp/$file"))[9] > $CONF{tempfile_del_hour} * 3600;
    }
    ### cidファイル、ログインセッションファイルの削除
    foreach my $dir(qw(login cid)) {
        opendir(DIR, "temp/$dir")
         or error("temp/$dirディレクトリが開けませんでした。: $!");
        foreach my $file(grep(/^\w+$/, readdir(DIR))) {
            ($file) = $file =~ /^(\w+)$/;
            unlink("temp/$dir/$file")
             if $time - (stat("temp/$dir/$file"))[9]
             > $CONF{cookie_expire_days} * 3600;
        }
    }
}

sub truncate_str {

    my($str, $length) = @_;
    my $truncated_str;
    foreach my $char($str =~ /[\x00-\x7f]|[\x8e\xa1-\xfe][\xa1-\xfe]|\x8f[\xa1-\xfe][\xa1-\xfe]/og) {
        return "$truncated_str..."
         if length($truncated_str) + length($char) > $length;
        $truncated_str .= $char;
    }
    return $truncated_str;
}

sub uri_escape {

    my $str = shift;
    $str =~ s/(\W)/'%' . unpack('H2', $1)/eg;
    return $str;

}

sub write_conf {

    my $ref = shift;
    open(W, "> tboard_conf.pl")
     or error("環境設定ファイル(tboard_conf.pl)への書き出しに失敗しました。: $!");
    print W <<__CONF_FILE_STR__;
#
# $ref->{prod_name} v$ref->{version} 環境設定ファイル
#
sub conf {

    my \%conf;

__CONF_FILE_STR__

    foreach (@{$CONF{write_conf_fields}}) {

        print W <<__CONF_FILE_STR__;
    chomp(\$conf{$_} = <<'_${_}_str_');
$ref->{$_}
_${_}_str_
__CONF_FILE_STR__

    }

    print W <<__CONF_FILE_STR__;
    \%conf;

}

1;
__CONF_FILE_STR__

    close(W);

}

sub view {

    #+----------------+----------------------+------------+
    #| 識別子(t)      | 表示タイプ           | ソート方法 |
    #+----------------+----------------------+------------+
    #| tree (default) | ツリー表示           | rd,lu      |
    #| thread         | スレッド表示         | lu         |
    #| list           | 投稿順(タイトル一覧) | msgno      |
    #| list2          | 〃(全表示)           | msgno      |
    #| topic          | トピック表示         | rd         |
    #+----------------+----------------------+------------+

    file_lock();

    my %rv; # return value

    (my $type = $FORM{t}) ||= "tree";
    my %allowed_t = map { $_ => 1 } qw(tree thread list list2 topic);
    $allowed_t{$type} or error("投稿一覧形式の指定(t)が正しくありません。");

    ### データの取り出しと全件数の取得
    my @tree;
    if ($type eq 'tree' or $type eq 'thread' or $type eq 'topic') {
        @tree = table_select("tboard_tree.cgi","",
         ($FORM{o} eq 'rd' or $type eq 'topic')
         ? "reg_date::desc" : "last_update::desc");
    } else {
        @tree = table_select("tboard_message.cgi","","msgno:num:desc");
    }
    $rv{cnt_all} = @tree;

    ### ページリンクの作成
    my $query = join("", map {"&$_=$FORM{$_}"} grep {$FORM{$_} ne ""} qw(t o));
    if ($FORM{p} > 0) {
        my $pre = $FORM{p} - $CONF{"page_disp_$type"};
        $rv{prev} = "<a href=$CONF{script_name}?p=$pre$query>$CONF{prev1str}</a>";
    } else {
        $rv{prev} = $CONF{prev0str};
    }
    if ($FORM{p} + $CONF{"page_disp_$type"} < $rv{cnt_all}) {
        my $nxt = $FORM{p} + $CONF{"page_disp_$type"};
        $rv{next} = "<a href=$CONF{script_name}?p=$nxt$query>$CONF{next1str}</a>";
    } else {
        $rv{next} = $CONF{next0str};
    }

    ### 現在のページと総ページ数の算出
    $rv{page_c} = $FORM{p} / $CONF{"page_disp_$type"} + 1;
    $rv{page_all} = int($rv{cnt_all} / $CONF{"page_disp_$type"})
                   + (($rv{cnt_all} % $CONF{"page_disp_$type"}) ? 1 : 0);

    ### ページ移動ナビの生成
    $rv{navi} = join("　", $rv{prev}, $rv{next}, ("[ " . join(" | ", map { $_==$rv{page_c} ? qq{<b>$_</b>} : (qq{<a href="$CONF{script_name}?p=} . ($CONF{"page_disp_$type"} * ($_ - 1)) . qq{$query">$_</a>}) } 1..$rv{page_all}) . " ]") );

    my %topic;
    if ($type eq 'topic') {
        my $idlist = join(",", map { "msgno=$_->{msgno}" } @tree);
        foreach my $ref(table_select("tboard_message.cgi","$idlist,stat=1")) {
            $topic{$ref->{msgno}} = $ref;
        }
    }

    my $cnt;
    my $p = $FORM{p};
    foreach my $ref(@tree) {
        next if $p-- > 0;
        last if ++$cnt > $CONF{"page_disp_$type"};
        if ($type eq 'tree') {
            $rv{list} .= mk_tree($ref->{tno}) . "<p>\n";
        } elsif ($type eq 'thread') {
            my ($link, $list) = mk_thread($ref->{tno});
            $rv{list} .= $list;
            $rv{link} .= $link;
        } elsif ($type eq 'topic') {
            $rv{list} .= mk_topic($topic{$ref->{tno}},$ref->{message_cnt});
        } elsif ($type eq 'list') {
            $rv{list} .= mk_list($ref) . "<p>\n";
        } else {
            $rv{list} .= mk_shousai_html($ref->{msgno}, $ref) . "<p>\n";
        }
    }

    $rv{list} ||= "<br>投稿データはありません。<p>";
    $rv{list} = $CONF{list_header}->{$type} . $rv{list} . $CONF{list_footer}->{$type};
    foreach (qw(body_text body_bgcolor)) {
        $rv{list} =~ s/##$_##/$CONF{$_}/g;
    }
    $rv{navi_bar} = mk_navi_bar($type, %FORM);

    # シリアルIDチェック
    $FORM{sid} = get_cookie("TBOARD_CID");

    set_cid();
    print _header("投稿一覧");
    print <<HTML;
<table class=description>
<tr><td>$CONF{description}</td></tr>
</table>

$rv{navi_bar}
<table border=0 cellpadding=5 cellspacing=0 width=700 style="border-bottom-style:solid;border-bottom-width:1px;border-color:$CONF{body_text};">
<tr><td><span style=font-size:9pt;>$rv{navi}</span></td></tr></table>
<p>
$rv{list}

<table border=0 cellpadding=5 cellspacing=0 width=700 style="border-top-style:solid;border-top-width:1px;border-color:$CONF{body_text};">
<tr><td><span style=font-size:9pt;>$rv{navi}</span></td></tr></table>
$rv{navi_bar}
HTML
    print _footer("no_border");

    exit;

}

sub view2 {

    $FORM{view2} or error("投稿番号を指定してください。");

    my $str = mk_shousai_html($FORM{view2});

    set_cid();
    print _header();
    print $str;
    print _footer();
    exit;


}

sub view_icon {

    my @icon_list = split(/\n/, $CONF{icon_list});
    my @icon_list_str = split(/\n/, $CONF{icon_list_str});
    my $list;

    foreach my $i(0..$#icon_list) {
        $list .= "<tr>\n" unless $i % 4;
        $list .= <<HTML;
<td bgcolor=$CONF{body_bgcolor}><img src="img/icon/$icon_list[$i]"></td>
<td bgcolor=$CONF{body_bgcolor}>$icon_list_str[$i]</td>
HTML
        $list .= "</tr>\n" if $i % 4 == 3;

    }
    if (@icon_list % 4) {
        foreach (1..(4 - @icon_list % 4)) {
            $list .= "<td bgcolor=$CONF{body_bgcolor} colspan=2>　</td>\n";
        }
    }
    print _header("アイコン一覧");
    print <<HTML;
<p><table border=0 cellpadding=0 cellspacing=0 bgcolor=$CONF{body_text} align=center>
<tr><td><table border=0 cellpadding=3 cellspacing=1>
HTML
    print $list;
    print "</td></tr></table></td></tr></table><p>\n";
    print "<div align=center><a href=javascript:window.close()>ウインドウを閉じる</a></div><p>\n";
    print _footer();
    exit;

}
