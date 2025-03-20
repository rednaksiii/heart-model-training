using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class HeartTracker : MonoBehaviour
{
    private UdpClient udpClient;
    private IPEndPoint remoteEndPoint;
    private float x, y, z, roll, pitch, yaw;

    void Start()
    {
        udpClient = new UdpClient(5065);  // Match Python's port
        remoteEndPoint = new IPEndPoint(IPAddress.Any, 5065);
        udpClient.BeginReceive(new AsyncCallback(ReceiveData), null);
    }

    void Update()
    {
        // Update the VR heart's position and rotation
        transform.position = new Vector3(x / 100, y / 100, z / 100);  // Scale appropriately
        transform.rotation = Quaternion.Euler(pitch, yaw, roll);
    }

    private void ReceiveData(IAsyncResult result)
    {
        byte[] receivedBytes = udpClient.EndReceive(result, ref remoteEndPoint);
        string receivedString = Encoding.UTF8.GetString(receivedBytes);

        // Parse JSON data
        try
        {
            HeartData data = JsonUtility.FromJson<HeartData>(receivedString);
            x = data.x;
            y = data.y;
            z = data.z;
            roll = data.roll;
            pitch = data.pitch;
            yaw = data.yaw;
        }
        catch (Exception e)
        {
            Debug.LogError("Error parsing JSON: " + e.Message);
        }

        // Continue listening
        udpClient.BeginReceive(new AsyncCallback(ReceiveData), null);
    }
}

// Define data structure for JSON parsing
[Serializable]
public class HeartData
{
    public float x;
    public float y;
    public float z;
    public float roll;
    public float pitch;
    public float yaw;
}
