namespace CouchTableController
{
    public struct RGBColor
    {
        public static RGBColor Black = new RGBColor(0, 0, 0);

        public byte R;
        public byte G;
        public byte B;

        public RGBColor(byte r, byte g, byte b)
        {
            this.R = r;
            this.G = g;
            this.B = b;
        }
    }
}