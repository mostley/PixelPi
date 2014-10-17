namespace CouchTableController
{
    using System;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    public class PostArrayHandler
    {
        private static readonly Regex s_ArrayRegex = new Regex(@"^([^\[]+)\[([^\]]+)\]\[([^\]]?)\]$");

        public static RGBColor[] ParseForm(dynamic form)
        {
            var result = new List<RGBColor>();

            var memberNames = (IEnumerable<string>)form.GetDynamicMemberNames();

            foreach (var key in memberNames)
            {
                string value = form[key];

                var match = s_ArrayRegex.Match(key);
                if (match.Success)
                {
                    string arrayName = match.Groups[1].Value;

                    if (arrayName == "leds")
                    {
                        var index = int.Parse(match.Groups[2].Value);

                        while (result.Count <= index)
                        {
                            result.Add(RGBColor.Black);
                        }

                        var propertyName = match.Groups[3].Value;

                        result[index] = SetValue(result[index], propertyName, value);
                    }
                    else
                    {
                        Console.WriteLine("Strange array found ('" + arrayName + "')");
                    }
                }
            }

            return result.ToArray();
        }

        private static RGBColor SetValue(RGBColor rgbColor, string propertyName, string value)
        {
            switch (propertyName)
            {
                case "R":
                    rgbColor.R = (byte)CClamp(int.Parse(value));
                    break;
                case "G":
                    rgbColor.G = (byte)CClamp(int.Parse(value));
                    break;
                case "B":
                    rgbColor.B = (byte)CClamp(int.Parse(value));
                    break;
            }

            return rgbColor;
        }

        private static int CClamp(int c)
        {
            return c < 0 ? 0 : (c > 255 ? 255 : c);
        }
    }
}