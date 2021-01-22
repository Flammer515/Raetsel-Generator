#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QKeyEvent>
#include <QEvent>
#include <QDebug>
QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
Ui::MainWindow *ui;
private slots:





    void on_Start_clicked();
    void on_chooseFile_clicked();

    void on_btn_tmp_up_clicked();
    void on_btn_tmp_down_clicked();
    void on_btnhummidity_up_clicked();
    void on_btnhumidity_down_clicked();

    void on_submit_clicked();
    void on_pushButton_clicked();
    void on_btnXup_clicked();
    void on_btnYdown_clicked();
    void on_btnXdown_clicked();
    void on_btnYup_clicked();
    void on_btnLichtAn_clicked();

    void on_farbenAuswahl_activated(int index);


};
#endif // MAINWINDOW_H
