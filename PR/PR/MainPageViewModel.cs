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
using Windows.Web.Http;

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

        private ObservableCollection<Data4Vis> dataVis = new ObservableCollection<Data4Vis>();
        public ObservableCollection<Data4Vis> DataVis
        {
            get => dataVis;
            set { dataVis = value; OnPropertyChanged(); }
        }

        //lzy
        private ObservableCollection<Data4Vis> trainDataVis1 = new ObservableCollection<Data4Vis>();
        public ObservableCollection<Data4Vis> TrainDataVis1
        {
            get => trainDataVis1;
            set { trainDataVis1 = value; OnPropertyChanged(); }
        }

        private ObservableCollection<Data4Vis> trainDataVis2 = new ObservableCollection<Data4Vis>();
        public ObservableCollection<Data4Vis> TrainDataVis2
        {
            get => trainDataVis2;
            set { trainDataVis2 = value; OnPropertyChanged(); }
        }

        private ObservableCollection<Data4Vis> trainDataVis3 = new ObservableCollection<Data4Vis>();
        public ObservableCollection<Data4Vis> TrainDataVis3
        {
            get => trainDataVis3;
            set { trainDataVis3 = value; OnPropertyChanged(); }
        }

        private ObservableCollection<Data4Vis> trainDataVis4 = new ObservableCollection<Data4Vis>();
        public ObservableCollection<Data4Vis> TrainDataVis4
        {
            get => trainDataVis4;
            set { trainDataVis4 = value; OnPropertyChanged(); }
        }

        private ObservableCollection<Data4Vis> testDataVis1 = new ObservableCollection<Data4Vis>();
        public ObservableCollection<Data4Vis> TestDataVis1
        {
            get => testDataVis1;
            set { testDataVis1 = value; OnPropertyChanged(); }
        }

        private ObservableCollection<Data4Vis> testDataVis2 = new ObservableCollection<Data4Vis>();
        public ObservableCollection<Data4Vis> TestDataVis2
        {
            get => testDataVis2;
            set { testDataVis2 = value; OnPropertyChanged(); }
        }

        private ObservableCollection<Data4Vis> testDataVis3 = new ObservableCollection<Data4Vis>();
        public ObservableCollection<Data4Vis> TestDataVis3
        {
            get => testDataVis3;
            set { testDataVis3 = value; OnPropertyChanged(); }
        }

        private ObservableCollection<Data4Vis> testDataVis4 = new ObservableCollection<Data4Vis>();
        public ObservableCollection<Data4Vis> TestDataVis4
        {
            get => testDataVis4;
            set { testDataVis4 = value; OnPropertyChanged(); }
        }
        //lzy

        private int classifierSelectIndex = 0;
        public int ClassifierSelectIndex
        {
            get => classifierSelectIndex;
            set { classifierSelectIndex = value; OnPropertyChanged(); }
        }

        private ObservableCollection<string> datatypeSelect = new ObservableCollection<string>();
        public ObservableCollection<string> DatatypeSelect
        {
            get => datatypeSelect;
            set { datatypeSelect = value; OnPropertyChanged(); }
        }

        private int datatypeSelectIndex = 0;
        public int DatatypeSelectIndex
        {
            get => datatypeSelectIndex;
            set { datatypeSelectIndex = value; OnPropertyChanged(); }
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

        private double sigma;
        public double Sigma
        {
            get => sigma;
            set { sigma = value; OnPropertyChanged(); }
        }

        private int predictLabel;
        public int PredictLabel
        {
            get => predictLabel;
            set { predictLabel = value; OnPropertyChanged(); }
        }

        private int numClasses;
        public int NumClasses
        {
            get => numClasses;
            set { numClasses = value; OnPropertyChanged(); }
        }

        private int numSamplePerClass;
        public int NumSamplePerClass
        {
            get => numSamplePerClass;
            set { numSamplePerClass = value; OnPropertyChanged(); }
        }
        #endregion


        public List<Data> traindatas = new List<Data>();
        public List<Data> testdatas = new List<Data>();
        string serverip = "127.0.0.1:5000";
        RecvData curr_recv_data = new RecvData();

       



        //public void AddTrainData()
        //{
        //    Data tempdata = new Data();
        //    tempdata.x = AddX;
        //    tempdata.y = AddY;
        //    tempdata.label = AddLabel;
        //    traindatas.Add(tempdata);
        //    FormatDataDisplay();
        //}

        //public void AddTestData()
        //{
        //    Data tempdata = new Data();
        //    tempdata.x = AddX;
        //    tempdata.y = AddY;
        //    tempdata.label = AddLabel;
        //    testdatas.Add(tempdata);
        //    FormatDataDisplay();
        //}


        public async void Predict()
        {
            Data tempdata = new Data();
            tempdata.x = AddX;
            tempdata.y = AddY;


            SendData senddata = new SendData();
            senddata.testdata.Add(tempdata);
            senddata.request_type = "Predict";
            senddata.classifiertype = ClassifierSelectIndex;

            string send = JsonConvert.SerializeObject(senddata);
            try
            {
                await SendInfo(send);
                PredictLabel = curr_recv_data.pred_labels[0];
            }
            catch
            { }

        }

        public void GenerateData()
        {
            List<Data> list_center = new List<Data>();
            Data temp_center = new Data();
            for (int i = 0; i < NumClasses; i++)
            {
                temp_center.x = i;
                temp_center.y = i % 2;
                temp_center.label = i;
                list_center.Add(temp_center.Copy());
            }
            if (DatatypeSelectIndex == 0)
            {
                GenerateGaussianSample(traindatas, DataVis, list_center, NumSamplePerClass, Sigma);
                Data4Vis temp_datavis = new Data4Vis();
                temp_datavis.x = 1;
                temp_datavis.y = 1;
                temp_datavis.label = 1;

                DataVis.Add(temp_datavis);

            }
            else
                GenerateGaussianSample(testdatas, DataVis, list_center, NumSamplePerClass, Sigma);
            FormatDataDisplay();

            //lzy
            TrainDataClass(DataVis);
            //lzy
        }

        public void ClearData()
        {
            traindatas = new List<Data>();
            testdatas = new List<Data>();
            DataVis.Clear();
            FormatDataDisplay();
        }

        public async void Train()
        {
            SendData senddata = new SendData();
            senddata.traindata = traindatas;
            senddata.request_type = "Train";
            senddata.classifiertype = ClassifierSelectIndex;

            string send = JsonConvert.SerializeObject(senddata);
            try
            {
                await SendInfo(send);
                TrainAccuracy = curr_recv_data.train_accuracy;
            }
            catch
            { }

        }

        public async void Test()
        {
            SendData senddata = new SendData();
            senddata.testdata = testdatas;
            senddata.request_type = "Test";
            senddata.classifiertype = ClassifierSelectIndex;

            string send = JsonConvert.SerializeObject(senddata);
            try
            {
                await SendInfo(send);
                TestAccuracy = curr_recv_data.test_accuracy;
            }
            catch
            { }

        }

        public async void Scan()
        {
            Data tempdata = new Data();
            SendData senddata = new SendData();
            List<int> predictlabels = new List<int>();
            for (int i = 0; i < 4 / 0.2; i++)
                for (int j = 0; j < 3 / 0.2; j++)
                {
                    tempdata.x = 0.2 * i;
                    tempdata.y = 0.2 * j;
                    senddata.testdata.Add(tempdata.Copy());
                }
            senddata.request_type = "Predict";
            senddata.classifiertype = ClassifierSelectIndex;

            string send = JsonConvert.SerializeObject(senddata);
            try
            {
                await SendInfo(send);
                predictlabels = curr_recv_data.pred_labels;
            }
            catch
            { }
        }


        #region Utility functions
        public void FormatDataDisplay()
        {
            string formatteddata = "Train Data\n[x, y]: label\n";
            foreach (Data sample in traindatas)
            {
                formatteddata += string.Format("[{0:F2}, {1:F2}]: {2}\n", sample.x, sample.y, sample.label);
            }
            formatteddata += "\nTest Data\n[x, y]: label\n";
            foreach (Data sample in testdatas)
            {
                formatteddata += string.Format("[{0:F2}, {1:F2}]: {2}\n", sample.x, sample.y, sample.label);
            }
            DataDisplay = formatteddata;
        }

        public async Task SendInfo(string send)
        {
            string str_uri = string.Format("http://{0}/post", serverip);
            RecvData temp_recv_data = new RecvData();

            HttpResponseMessage httpresponse = new HttpResponseMessage();
            string httpresponsebody;
            Uri requestUri = new Uri(str_uri);
            HttpClient httpclient = new HttpClient();

            try
            {
                httpclient.DefaultRequestHeaders.Accept.Add(new Windows.Web.Http.Headers.HttpMediaTypeWithQualityHeaderValue("application/json"));
                httpresponse = await httpclient.PostAsync(requestUri, new HttpStringContent(send, Windows.Storage.Streams.UnicodeEncoding.Utf8, "application/json"));

                httpresponsebody = await httpresponse.Content.ReadAsStringAsync();

                //TODO
                temp_recv_data = JsonConvert.DeserializeObject<RecvData>(httpresponsebody);
                curr_recv_data = temp_recv_data;

            }
            catch (Exception ex)
            {
                httpresponsebody = JsonConvert.SerializeObject("Error: " + ex.HResult.ToString("x") + "Message: " + ex.Message);
                DisplayDialog("Connection failed", "Please check server IP address and your network status and try again");
                throw (ex);

            }
        }

        private async void DisplayDialog(string title, string content)
        {
            ContentDialog noWifiDialog = new ContentDialog
            {
                Title = title,
                Content = content,
                CloseButtonText = "Ok"
            };
            try
            {
                ContentDialogResult result = await noWifiDialog.ShowAsync();
            }
            catch
            {

            }
        }

        private void GenerateGaussianSample(List<Data> list_data, ObservableCollection<Data4Vis> list_datavis, List<Data> center, int num_sample, double sigma)
        {
            Random random = new Random();
            Data temp_data = new Data();
            Data4Vis temp_datavis = new Data4Vis();
            for (int i = 0; i < num_sample; i++)
            {
                foreach (Data curr_center in center)
                {
                    temp_data.x = SampleGaussian(random, curr_center.x, sigma);
                    temp_data.y = SampleGaussian(random, curr_center.y, sigma);
                    temp_data.label = curr_center.label;
                    list_data.Add(temp_data.Copy());

                    temp_datavis.x = temp_data.x;
                    temp_datavis.y = temp_data.y;
                    temp_datavis.label = curr_center.label;
                    list_datavis.Add(temp_datavis.Copy());
                }
            }
        }

        private static double SampleGaussian(Random random, double mean, double stddev)
        {
            // The method requires sampling from a uniform random of (0,1]
            // but Random.NextDouble() returns a sample of [0,1).
            double x1 = 1 - random.NextDouble();
            double x2 = 1 - random.NextDouble();

            double y1 = Math.Sqrt(-2.0 * Math.Log(x1)) * Math.Cos(2.0 * Math.PI * x2);
            return y1 * stddev + mean;
        }

        public void TrainDataClass(ObservableCollection<Data4Vis> Data)
        {
            TrainDataVis1.Clear();
            TrainDataVis2.Clear();
            TrainDataVis3.Clear();
            TrainDataVis4.Clear();
            foreach (Data4Vis tempdata in Data)
                switch (tempdata.label)
                {
                    case 0:
                        TrainDataVis1.Add(tempdata);
                        break;
                    case 1:
                        TrainDataVis2.Add(tempdata);
                        break;
                    case 2:
                        TrainDataVis3.Add(tempdata);
                        break;
                    case 3:
                        TrainDataVis4.Add(tempdata);
                        break;
                    default:

                        break;
                }                    
        }

        public void TestDataClass(ObservableCollection<Data4Vis> Data)
        {
            TestDataVis1.Clear();
            TestDataVis2.Clear();
            TestDataVis3.Clear();
            TestDataVis4.Clear();
            foreach (Data4Vis tempdata in Data)
                switch (tempdata.label)
                {
                    case 0:
                        TestDataVis1.Add(tempdata);
                        break;
                    case 1:
                        TestDataVis2.Add(tempdata);
                        break;
                    case 2:
                        TestDataVis3.Add(tempdata);
                        break;
                    case 3:
                        TestDataVis4.Add(tempdata);
                        break;
                    default:

                        break;
                }
        }

        #endregion

    }
}
