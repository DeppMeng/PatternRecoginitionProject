using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Meowtrix.ComponentModel;
using Windows.UI.Xaml;
using Newtonsoft.Json;
using System.Collections.ObjectModel;
using Windows.Storage;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Controls;

namespace PR
{
    public class MainPageViewModel : NotificationObject
    {
        #region ViewModel Definitions
        private ObservableCollection<string> classifierSelect = new ObservableCollection<string>();
        public ObservableCollection<string> ClassifierSelect
        {
            get => classifierSelect;
            set { classifierSelect = value; OnPropertyChanged(); }
        }

        private int classifierSelectIndex = 0;
        public int ClassifierSelectIndex
        {
            get => classifierSelectIndex;
            set { classifierSelectIndex = value; OnPropertyChanged(); }
        }

        private double testAccuracy;
        public double TestAccuracy
        {
            get => testAccuracy;
            set { testAccuracy = value; OnPropertyChanged(); }
        }

        private double trainAccuracy;
        public double TrainAccuracy
        {
            get => trainAccuracy;
            set { trainAccuracy = value; OnPropertyChanged(); }
        }

        private string dataDisplay;
        public string DataDisplay
        {
            get => dataDisplay;
            set { dataDisplay = value; OnPropertyChanged(); }
        }

        private double addX;
        public double AddX
        {
            get => addX;
            set { addX = value; OnPropertyChanged(); }
        }

        private double addY;
        public double AddY
        {
            get => addY;
            set { addY = value; OnPropertyChanged(); }
        }

        private double addLabel;
        public double AddLabel
        {
            get => addLabel;
            set { addLabel = value; OnPropertyChanged(); }
        }
        #endregion

        public async void AddTrainData()
        {

        }

        public async void AddTestData()
        {

        }


        #region Utility functions
        private string FormatDataDisplay(List<Data> data)
        {
            string formatteddata = "[x, y]: label";
            foreach (Data sample in data)
            {
                formatteddata += string.Format("[{0}, {1}]: {2}\n", sample.x, sample.y, sample.label);
            }
            return formatteddata;
        }

        #endregion

    }
}
