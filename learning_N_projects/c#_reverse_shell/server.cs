using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Net;

namespace ServerSocket
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int buff_size = 2048;

            // Setting up the socket and accepting the connection:
            IPEndPoint iP = new IPEndPoint(IPAddress.Any, 1234);
            Socket ss = new Socket(IPAddress.Any.AddressFamily,SocketType.Stream,ProtocolType.Tcp);
            ss.Bind(iP);
            ss.Listen(5);
            Console.WriteLine("[!] Listening for a connection...");
            Socket cs = ss.Accept();
            Console.WriteLine("[+] Connection from {0}", cs.RemoteEndPoint);

            //Sending and receiving stuff:
            byte[] b = new byte[buff_size];

            Console.Write("$> ");
            string msg = Console.ReadLine();
            cs.Send(Encoding.ASCII.GetBytes(msg));
            while(msg != "quit")
            {
                Array.Clear(b, 0, b.Length);
                cs.Receive(b);
                msg = Encoding.ASCII.GetString(b).TrimEnd('\0');
                Console.WriteLine("The Client said: {0}", msg);

                Console.Write("$> ");
                msg = Console.ReadLine();
                cs.Send(Encoding.ASCII.GetBytes(msg));
            }

            //Finishing up:
            cs.Close();
            ss.Close();

        }
    }
}
