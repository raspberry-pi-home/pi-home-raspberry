import express from 'express'

// @ts-ignore TS7006
export const api = (db, board) => {
  const router = express.Router()

  // list all devices
  router.get('/devices', (req, res) => {
    const devices = board.getDevices()

    if (req.query?.type === 'led' || req.query?.type === 'button') {
      // @ts-ignore TS7006
      return res.json(devices.filter(device => device.type && device.type.toLowerCase().endsWith(req.query.type)))
    }

    res.json(devices)
  })

  // change device status (by pin)
  router.post('/devices/change-status', (req, res) => {
    res.json({ status: board.changeDeviceStatus(+req.body.pin) })
  })

  // list all available devices
  router.get('/devices/available', (req, res) => {
    res.json(board.getAvailableDevices())
  })

  // create a device
  router.post('/devices', (req, res) => {
    const device = {
      pin: +req.body.pin,
      label: req.body.label,
      type: req.body.type,
    }

    board.addDevice(device)

    db.get('devices').push(device).write()

    res.json(board.getDevice(+req.body.pin))
  })

  // get a device
  router.get('/devices/:pin', (req, res) => {
    res.json(board.getDevice(+req.params.pin))
  })

  // modify a device
  router.put('/devices/:pin', (req, res) => {
    board.editDevice(+req.params.pin, { label: req.body.label })

    db.get('devices')
      .find({ pin: +req.params.pin })
      .assign({ label: req.body.label })
      .write()

    res.json(board.getDevice(+req.params.pin))
  })

  // delete a device
  router.delete('/devices/:pin', (req, res) => {
    board.deleteDevice(+req.params.pin)

    db.get('devices').remove({ pin: +req.params.pin }).write()

    res.json(board.getDevices())
  })

  // link an input device to an output device
  router.post('/devices/link/:inputPin/:outputPin', (req, res) => {
    const dependency = {
      inputPin: +req.params.inputPin,
      outputPin: +req.params.outputPin,
    }

    board.linkDevices(dependency)

    db.get('dependencies').push(dependency).write()

    res.json(dependency)
  })

  // unlink an input device from the output device
  router.post('/devices/unlink/:inputPin/:outputPin', (req, res) => {
    const dependency = {
      inputPin: +req.params.inputPin,
      outputPin: +req.params.outputPin,
    }

    board.unlinkDevices(dependency)

    db.get('dependencies').remove({ inputPin: +req.params.inputPin, outputPin: +req.params.outputPin }).write()

    res.json(dependency)
  })

  // debug
  router.get('/_debug', (req, res) => {
    res.json({
      board,
      db,
    })
  })

  return router
}
