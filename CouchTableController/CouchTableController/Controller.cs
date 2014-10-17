namespace CouchTableController
{
    using System;
    using System.Net;
    using System.Net.Sockets;
    using Nancy;
    using HttpStatusCode = Nancy.HttpStatusCode;

    public class Controller : NancyModule
    {
        private static readonly RGBColor[] s_Leds = new RGBColor[105];

        public Controller()
        {
            Get["/"] = x => View["index"];
            Get["/index.html"] = x => View["index.html"];
            Get["/follow.html"] = x => View["follow.html"];
            Get["/pong.html"] = x => View["pong.html"];

            Get["/leds"] = x => s_Leds;
            Post["/leds"] = parameters =>
            {
                var data = PostArrayHandler.ParseForm(this.Request.Form);
                for (int i = 0; i < data.Length; i++)
                {
                    s_Leds[i] = data[i];
                }

                return DoUpdate();
            };
        }

        HttpStatusCode DoUpdate()
        {
            var result = HttpStatusCode.OK;

            try
            {
                var socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
                var data = ToByteArray();
                socket.SendTo(data, new IPEndPoint(IPAddress.Parse("192.168.1.5"), 6803));
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
                result = HttpStatusCode.InternalServerError;
            }

            return result;
        }

        private byte[] ToByteArray()
        {
            var result = new byte[s_Leds.Length * 3];

            const int pixelsize = 3;
            const int width = 12;
            const int height = 8;

            int j = 0;

            while (j < width * height * pixelsize)
            {
                var y = j / pixelsize % height;
                var x = (int)Math.Floor((double)j / pixelsize / height);

                int ledIndex;
                if (x % 2 == 0)
                {
                    ledIndex = ((width - 1) - x) + y * width;
                }
                else
                {
                    ledIndex = ((width - 1) - x) + ((height - 1) - y) * width;
                }

                var led = s_Leds[ledIndex];
                result[j] = CClamp(led.R);
                result[j + 1] = CClamp(led.G);
                result[j + 2] = CClamp(led.B);

                j += 3;
            }

            var k = 95 * 3;
            for (int i = 96; i < 105; i++)
            {
                var led = s_Leds[i];
                result[k] = CClamp(led.R);
                result[k + 1] = CClamp(led.G);
                result[k + 2] = CClamp(led.B);

                k += 3;
            }

            return result;
        }

        private byte CClamp(byte c)
        {
            return (byte) (c > 255 ? 255 : c);
        }
    }
}