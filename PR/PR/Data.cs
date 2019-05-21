using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PR
{
    public class Data
    {
        public double x;
        public double y;
        public double label;

        public Data Copy()
        {
            Data copy_data = new Data();
            copy_data.x = x;
            copy_data.y = y;
            copy_data.label = label;
            return copy_data;
        }

    }
}
