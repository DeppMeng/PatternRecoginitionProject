using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PR
{
    public class SendData
    {
        public List<Data> traindata = new List<Data>();
        public List<Data> testdata = new List<Data>();
        public int classifiertype;
        public string request_type;
    }
}
