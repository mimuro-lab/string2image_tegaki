# 文字列を手書き画像に変換するプログラム

このプログラムは、string.txtに保存された文字列を、一行ずつ取り出して、手書きの画像を自動生成するプログラムである。

使用したデータセットは以下の3つである。

* ETL6(日本語のカタカナ、大文字のアルファベット)
* ETL9G(日本語、標準JIS第二種漢字、ひらがな)
* matlabのemnist(小文字のアルファベットのため)

# 使用方法

1. ディレクトリETL6にETL6のバイナリファイルを入れる
2. ディレクトリETL6にあるmake_etl_table.pyを実行する
3. ディレクトリETL9GにETL9Gのバイナリファイルを入れる
4. ディレクトリETL9Gにあるmake_etl_table.pyを実行する
5. ディレクトリemnistにemnist-byclass.matを入れる
6. ディレクトリemnistにあるmake_table.pyを実行する
7. ディレクトリETL6とETL9Gとemnistの中身を全てディレクトリETLに入れる
8. strings.txtに作成する文字列を書き込む
9. make_image.pyを実行する
