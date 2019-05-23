using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PR
{
    public class Data4Vis
    {
        private double x_;
        private double y_;
        private double label_;

        public double x
        {
            get { return x_; }
            set { x_ = value; }
        }

        public double y
        {
            get { return y_; }
            set { y_ = value; }
        }

        public double label
        {
            get { return label_; }
            set { label_ = value; }
        }


        public Data4Vis Copy()
        {
            Data4Vis copy_data = new Data4Vis();
            copy_data.x = x;
            copy_data.y = y;
            copy_data.label = label;
            return copy_data;
        }

    }
}
