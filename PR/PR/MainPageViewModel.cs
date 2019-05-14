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

        private double testAccuracy = 0;
        public double TestAccuracy
        {
            get => testAccuracy;
            set { testAccuracy = value; OnPropertyChanged(); }
        }

        private double trainAccuracy = 0;
        public double TrainAccuracy
        {
            get => trainAccuracy;
            set { trainAccuracy = value; OnPropertyChanged(); }
        }

        #endregion


    }
}
