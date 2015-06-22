/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.4.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QGraphicsView>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *action_open_image;
    QAction *action_next;
    QAction *action_previous;
    QWidget *centralWidget;
    QGridLayout *gridLayout;
    QGraphicsView *graphics_view;
    QTabWidget *tabWidget;
    QWidget *tab_images;
    QVBoxLayout *verticalLayout_2;
    QListWidget *list_images;
    QWidget *tab_preprocess;
    QVBoxLayout *verticalLayout;
    QGroupBox *groupBox;
    QVBoxLayout *verticalLayout_3;
    QDoubleSpinBox *spin_resize;
    QGroupBox *color_filter;
    QGridLayout *gridLayout_2;
    QComboBox *color_selector;
    QPushButton *button_reload_color;
    QPushButton *button_save_color;
    QGroupBox *hsv_filter;
    QFormLayout *formLayout;
    QLabel *label_h;
    QHBoxLayout *horizontalLayout;
    QSlider *th;
    QSpinBox *spin_hue_min;
    QHBoxLayout *horizontalLayout_2;
    QSlider *tH;
    QSpinBox *spin_hue_max;
    QLabel *label_H;
    QHBoxLayout *horizontalLayout_3;
    QSlider *ts;
    QSpinBox *spin_sat_min;
    QLabel *label_s;
    QHBoxLayout *horizontalLayout_4;
    QSlider *tS;
    QSpinBox *spin_sat_max;
    QLabel *label_S;
    QHBoxLayout *horizontalLayout_5;
    QSlider *tv;
    QSpinBox *spin_val_min;
    QLabel *label_v;
    QHBoxLayout *horizontalLayout_6;
    QSlider *tV;
    QSpinBox *spin_val_max;
    QLabel *label_V;
    QSpacerItem *verticalSpacer;
    QWidget *tab_2;
    QGroupBox *groupBox_2;
    QVBoxLayout *verticalLayout_4;
    QComboBox *combo_output;
    QHBoxLayout *horizontalLayout_7;
    QSpacerItem *horizontalSpacer;
    QLabel *label_status;
    QMenuBar *menuBar;
    QMenu *menuFile;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(1005, 712);
        action_open_image = new QAction(MainWindow);
        action_open_image->setObjectName(QStringLiteral("action_open_image"));
        action_next = new QAction(MainWindow);
        action_next->setObjectName(QStringLiteral("action_next"));
        action_previous = new QAction(MainWindow);
        action_previous->setObjectName(QStringLiteral("action_previous"));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        graphics_view = new QGraphicsView(centralWidget);
        graphics_view->setObjectName(QStringLiteral("graphics_view"));

        gridLayout->addWidget(graphics_view, 0, 1, 2, 1);

        tabWidget = new QTabWidget(centralWidget);
        tabWidget->setObjectName(QStringLiteral("tabWidget"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Expanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(tabWidget->sizePolicy().hasHeightForWidth());
        tabWidget->setSizePolicy(sizePolicy);
        tab_images = new QWidget();
        tab_images->setObjectName(QStringLiteral("tab_images"));
        verticalLayout_2 = new QVBoxLayout(tab_images);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setContentsMargins(11, 11, 11, 11);
        verticalLayout_2->setObjectName(QStringLiteral("verticalLayout_2"));
        list_images = new QListWidget(tab_images);
        list_images->setObjectName(QStringLiteral("list_images"));

        verticalLayout_2->addWidget(list_images);

        tabWidget->addTab(tab_images, QString());
        tab_preprocess = new QWidget();
        tab_preprocess->setObjectName(QStringLiteral("tab_preprocess"));
        verticalLayout = new QVBoxLayout(tab_preprocess);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        groupBox = new QGroupBox(tab_preprocess);
        groupBox->setObjectName(QStringLiteral("groupBox"));
        verticalLayout_3 = new QVBoxLayout(groupBox);
        verticalLayout_3->setSpacing(6);
        verticalLayout_3->setContentsMargins(11, 11, 11, 11);
        verticalLayout_3->setObjectName(QStringLiteral("verticalLayout_3"));
        spin_resize = new QDoubleSpinBox(groupBox);
        spin_resize->setObjectName(QStringLiteral("spin_resize"));
        spin_resize->setDecimals(3);
        spin_resize->setMinimum(0.001);
        spin_resize->setSingleStep(0.05);
        spin_resize->setValue(0.45);

        verticalLayout_3->addWidget(spin_resize);


        verticalLayout->addWidget(groupBox);

        color_filter = new QGroupBox(tab_preprocess);
        color_filter->setObjectName(QStringLiteral("color_filter"));
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(color_filter->sizePolicy().hasHeightForWidth());
        color_filter->setSizePolicy(sizePolicy1);
        gridLayout_2 = new QGridLayout(color_filter);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setContentsMargins(11, 11, 11, 11);
        gridLayout_2->setObjectName(QStringLiteral("gridLayout_2"));
        color_selector = new QComboBox(color_filter);
        color_selector->setObjectName(QStringLiteral("color_selector"));
        QSizePolicy sizePolicy2(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(0);
        sizePolicy2.setHeightForWidth(color_selector->sizePolicy().hasHeightForWidth());
        color_selector->setSizePolicy(sizePolicy2);

        gridLayout_2->addWidget(color_selector, 0, 0, 1, 2);

        button_reload_color = new QPushButton(color_filter);
        button_reload_color->setObjectName(QStringLiteral("button_reload_color"));

        gridLayout_2->addWidget(button_reload_color, 1, 0, 1, 1);

        button_save_color = new QPushButton(color_filter);
        button_save_color->setObjectName(QStringLiteral("button_save_color"));

        gridLayout_2->addWidget(button_save_color, 1, 1, 1, 1);


        verticalLayout->addWidget(color_filter);

        hsv_filter = new QGroupBox(tab_preprocess);
        hsv_filter->setObjectName(QStringLiteral("hsv_filter"));
        sizePolicy1.setHeightForWidth(hsv_filter->sizePolicy().hasHeightForWidth());
        hsv_filter->setSizePolicy(sizePolicy1);
        formLayout = new QFormLayout(hsv_filter);
        formLayout->setSpacing(6);
        formLayout->setContentsMargins(11, 11, 11, 11);
        formLayout->setObjectName(QStringLiteral("formLayout"));
        label_h = new QLabel(hsv_filter);
        label_h->setObjectName(QStringLiteral("label_h"));

        formLayout->setWidget(0, QFormLayout::LabelRole, label_h);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        horizontalLayout->setContentsMargins(-1, 0, -1, -1);
        th = new QSlider(hsv_filter);
        th->setObjectName(QStringLiteral("th"));
        th->setMinimumSize(QSize(200, 0));
        th->setMaximum(180);
        th->setOrientation(Qt::Horizontal);

        horizontalLayout->addWidget(th);

        spin_hue_min = new QSpinBox(hsv_filter);
        spin_hue_min->setObjectName(QStringLiteral("spin_hue_min"));
        spin_hue_min->setMaximum(180);

        horizontalLayout->addWidget(spin_hue_min);


        formLayout->setLayout(0, QFormLayout::FieldRole, horizontalLayout);

        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setSpacing(6);
        horizontalLayout_2->setObjectName(QStringLiteral("horizontalLayout_2"));
        horizontalLayout_2->setContentsMargins(-1, 0, 0, -1);
        tH = new QSlider(hsv_filter);
        tH->setObjectName(QStringLiteral("tH"));
        QSizePolicy sizePolicy3(QSizePolicy::Expanding, QSizePolicy::Fixed);
        sizePolicy3.setHorizontalStretch(0);
        sizePolicy3.setVerticalStretch(0);
        sizePolicy3.setHeightForWidth(tH->sizePolicy().hasHeightForWidth());
        tH->setSizePolicy(sizePolicy3);
        tH->setMinimumSize(QSize(200, 0));
        tH->setMaximum(180);
        tH->setOrientation(Qt::Horizontal);

        horizontalLayout_2->addWidget(tH);

        spin_hue_max = new QSpinBox(hsv_filter);
        spin_hue_max->setObjectName(QStringLiteral("spin_hue_max"));
        spin_hue_max->setMaximum(180);

        horizontalLayout_2->addWidget(spin_hue_max);


        formLayout->setLayout(2, QFormLayout::FieldRole, horizontalLayout_2);

        label_H = new QLabel(hsv_filter);
        label_H->setObjectName(QStringLiteral("label_H"));

        formLayout->setWidget(2, QFormLayout::LabelRole, label_H);

        horizontalLayout_3 = new QHBoxLayout();
        horizontalLayout_3->setSpacing(6);
        horizontalLayout_3->setObjectName(QStringLiteral("horizontalLayout_3"));
        ts = new QSlider(hsv_filter);
        ts->setObjectName(QStringLiteral("ts"));
        ts->setMinimumSize(QSize(200, 0));
        ts->setMaximum(256);
        ts->setOrientation(Qt::Horizontal);

        horizontalLayout_3->addWidget(ts);

        spin_sat_min = new QSpinBox(hsv_filter);
        spin_sat_min->setObjectName(QStringLiteral("spin_sat_min"));
        spin_sat_min->setMaximum(255);

        horizontalLayout_3->addWidget(spin_sat_min);


        formLayout->setLayout(4, QFormLayout::FieldRole, horizontalLayout_3);

        label_s = new QLabel(hsv_filter);
        label_s->setObjectName(QStringLiteral("label_s"));

        formLayout->setWidget(4, QFormLayout::LabelRole, label_s);

        horizontalLayout_4 = new QHBoxLayout();
        horizontalLayout_4->setSpacing(6);
        horizontalLayout_4->setObjectName(QStringLiteral("horizontalLayout_4"));
        tS = new QSlider(hsv_filter);
        tS->setObjectName(QStringLiteral("tS"));
        tS->setMinimumSize(QSize(200, 0));
        tS->setMaximum(256);
        tS->setOrientation(Qt::Horizontal);

        horizontalLayout_4->addWidget(tS);

        spin_sat_max = new QSpinBox(hsv_filter);
        spin_sat_max->setObjectName(QStringLiteral("spin_sat_max"));
        spin_sat_max->setMaximum(255);

        horizontalLayout_4->addWidget(spin_sat_max);


        formLayout->setLayout(5, QFormLayout::FieldRole, horizontalLayout_4);

        label_S = new QLabel(hsv_filter);
        label_S->setObjectName(QStringLiteral("label_S"));

        formLayout->setWidget(5, QFormLayout::LabelRole, label_S);

        horizontalLayout_5 = new QHBoxLayout();
        horizontalLayout_5->setSpacing(6);
        horizontalLayout_5->setObjectName(QStringLiteral("horizontalLayout_5"));
        tv = new QSlider(hsv_filter);
        tv->setObjectName(QStringLiteral("tv"));
        tv->setMinimumSize(QSize(200, 0));
        tv->setMaximum(256);
        tv->setOrientation(Qt::Horizontal);

        horizontalLayout_5->addWidget(tv);

        spin_val_min = new QSpinBox(hsv_filter);
        spin_val_min->setObjectName(QStringLiteral("spin_val_min"));
        spin_val_min->setMaximum(255);

        horizontalLayout_5->addWidget(spin_val_min);


        formLayout->setLayout(6, QFormLayout::FieldRole, horizontalLayout_5);

        label_v = new QLabel(hsv_filter);
        label_v->setObjectName(QStringLiteral("label_v"));

        formLayout->setWidget(6, QFormLayout::LabelRole, label_v);

        horizontalLayout_6 = new QHBoxLayout();
        horizontalLayout_6->setSpacing(6);
        horizontalLayout_6->setObjectName(QStringLiteral("horizontalLayout_6"));
        tV = new QSlider(hsv_filter);
        tV->setObjectName(QStringLiteral("tV"));
        tV->setMinimumSize(QSize(200, 0));
        tV->setMaximum(256);
        tV->setOrientation(Qt::Horizontal);

        horizontalLayout_6->addWidget(tV);

        spin_val_max = new QSpinBox(hsv_filter);
        spin_val_max->setObjectName(QStringLiteral("spin_val_max"));
        spin_val_max->setMaximum(255);

        horizontalLayout_6->addWidget(spin_val_max);


        formLayout->setLayout(7, QFormLayout::FieldRole, horizontalLayout_6);

        label_V = new QLabel(hsv_filter);
        label_V->setObjectName(QStringLiteral("label_V"));

        formLayout->setWidget(7, QFormLayout::LabelRole, label_V);


        verticalLayout->addWidget(hsv_filter);

        verticalSpacer = new QSpacerItem(0, 1000, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout->addItem(verticalSpacer);

        tabWidget->addTab(tab_preprocess, QString());
        tab_2 = new QWidget();
        tab_2->setObjectName(QStringLiteral("tab_2"));
        tabWidget->addTab(tab_2, QString());

        gridLayout->addWidget(tabWidget, 0, 0, 1, 1);

        groupBox_2 = new QGroupBox(centralWidget);
        groupBox_2->setObjectName(QStringLiteral("groupBox_2"));
        verticalLayout_4 = new QVBoxLayout(groupBox_2);
        verticalLayout_4->setSpacing(6);
        verticalLayout_4->setContentsMargins(11, 11, 11, 11);
        verticalLayout_4->setObjectName(QStringLiteral("verticalLayout_4"));
        combo_output = new QComboBox(groupBox_2);
        combo_output->setObjectName(QStringLiteral("combo_output"));

        verticalLayout_4->addWidget(combo_output);


        gridLayout->addWidget(groupBox_2, 1, 0, 1, 1);

        horizontalLayout_7 = new QHBoxLayout();
        horizontalLayout_7->setSpacing(6);
        horizontalLayout_7->setObjectName(QStringLiteral("horizontalLayout_7"));
        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_7->addItem(horizontalSpacer);

        label_status = new QLabel(centralWidget);
        label_status->setObjectName(QStringLiteral("label_status"));

        horizontalLayout_7->addWidget(label_status);


        gridLayout->addLayout(horizontalLayout_7, 2, 0, 1, 2);

        MainWindow->setCentralWidget(centralWidget);
        graphics_view->raise();
        tabWidget->raise();
        groupBox_2->raise();
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 1005, 19));
        menuFile = new QMenu(menuBar);
        menuFile->setObjectName(QStringLiteral("menuFile"));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        statusBar->setEnabled(true);
        statusBar->setSizeGripEnabled(true);
        MainWindow->setStatusBar(statusBar);

        menuBar->addAction(menuFile->menuAction());
        menuFile->addAction(action_open_image);
        menuFile->addAction(action_next);
        menuFile->addAction(action_previous);
        mainToolBar->addAction(action_next);
        mainToolBar->addAction(action_previous);

        retranslateUi(MainWindow);

        tabWidget->setCurrentIndex(0);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", 0));
        action_open_image->setText(QApplication::translate("MainWindow", "Open", 0));
        action_next->setText(QApplication::translate("MainWindow", "Next", 0));
#ifndef QT_NO_TOOLTIP
        action_next->setToolTip(QApplication::translate("MainWindow", "Next image", 0));
#endif // QT_NO_TOOLTIP
        action_previous->setText(QApplication::translate("MainWindow", "Previous", 0));
        tabWidget->setTabText(tabWidget->indexOf(tab_images), QApplication::translate("MainWindow", "Images", 0));
        groupBox->setTitle(QApplication::translate("MainWindow", "Resize factor", 0));
        color_filter->setTitle(QApplication::translate("MainWindow", "Color filter", 0));
        button_reload_color->setText(QApplication::translate("MainWindow", "Reload", 0));
        button_save_color->setText(QApplication::translate("MainWindow", "Save", 0));
        hsv_filter->setTitle(QApplication::translate("MainWindow", "HSV filter", 0));
        label_h->setText(QApplication::translate("MainWindow", "H min", 0));
        label_H->setText(QApplication::translate("MainWindow", "H max", 0));
        label_s->setText(QApplication::translate("MainWindow", "S min", 0));
        label_S->setText(QApplication::translate("MainWindow", "S max", 0));
        label_v->setText(QApplication::translate("MainWindow", "V min", 0));
        label_V->setText(QApplication::translate("MainWindow", "V max", 0));
        tabWidget->setTabText(tabWidget->indexOf(tab_preprocess), QApplication::translate("MainWindow", "Preprocess", 0));
        tabWidget->setTabText(tabWidget->indexOf(tab_2), QApplication::translate("MainWindow", "Identify", 0));
        groupBox_2->setTitle(QApplication::translate("MainWindow", "Output", 0));
        combo_output->clear();
        combo_output->insertItems(0, QStringList()
         << QApplication::translate("MainWindow", "Original", 0)
         << QApplication::translate("MainWindow", "Preprocess", 0)
         << QApplication::translate("MainWindow", "Identify", 0)
        );
        label_status->setText(QApplication::translate("MainWindow", "Status", 0));
        menuFile->setTitle(QApplication::translate("MainWindow", "File", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
