using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.ApplicationModel.Core;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI;
using Windows.UI.ViewManagement;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;
using Windows.Graphics.Display;
using WinRTXamlToolkit.Controls.DataVisualization.Charting;

// https://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x804 上介绍了“空白页”项模板

namespace PR
{
    /// <summary>
    /// 可用于自身或导航至 Frame 内部的空白页。
    /// </summary>
    public sealed partial class MainPage : Page
    {
        private MainPageViewModel ViewModel = new MainPageViewModel();
        public MainPage()
        {
            this.InitializeComponent();
            ApplicationViewTitleBar formattableTitleBar = ApplicationView.GetForCurrentView().TitleBar;
            formattableTitleBar.ButtonBackgroundColor = Colors.Transparent;
            CoreApplicationViewTitleBar coreTitleBar = CoreApplication.GetCurrentView().TitleBar;
            coreTitleBar.ExtendViewIntoTitleBar = true;

            ViewModel.ClassifierSelect.Add("Min Distance");
            ViewModel.ClassifierSelect.Add("Multi-layer Perceptron");
            ViewModel.TrainAccuracy = 0;
            ViewModel.TestAccuracy = 0;

            ViewModel.DatatypeSelect.Add("Train");
            ViewModel.DatatypeSelect.Add("Test");

            ViewModel.NumClasses = 1;
            ViewModel.NumSamplePerClass = 1;
            ViewModel.Sigma = 0.5;

            ViewModel.FormatDataDisplay();

           
        }
    }
}
